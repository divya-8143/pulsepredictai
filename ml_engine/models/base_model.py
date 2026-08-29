from abc import ABC, abstractmethod
import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List

class BaseHealthRiskModel(ABC):
    """
    Abstract Base Class defining standard interface for all PulsePredict clinical models.
    """
    def __init__(self, model_name: str, version: str = "v1.0.0"):
        self.model_name = model_name
        self.version = version
        self.model = None
        self.is_fitted = False
        self.feature_names = []

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: np.ndarray, **kwargs) -> "BaseHealthRiskModel":
        pass

    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        pass

    def predict_risk_score(self, X: pd.DataFrame) -> np.ndarray:
        """
        Compute calibrated 0.0 - 100.0 risk score from multi-class probabilities.
        Class weights: Low=0, Moderate=33.3, High=66.6, Critical=100.0
        """
        probs = self.predict_proba(X)
        if probs.shape[1] == 4:
            weights = np.array([10.0, 37.5, 62.5, 87.5])
            scores = np.dot(probs, weights)
        else:
            scores = probs[:, 1] * 100.0
        return np.clip(scores, 0.0, 100.0)

    def predict_category(self, X: pd.DataFrame) -> List[str]:
        scores = self.predict_risk_score(X)
        categories = []
        for s in scores:
            if s < 25.0:
                categories.append("LOW")
            elif s < 50.0:
                categories.append("MODERATE")
            elif s < 75.0:
                categories.append("HIGH")
            else:
                categories.append("CRITICAL")
        return categories

    @abstractmethod
    def get_feature_importances(self) -> Dict[str, float]:
        pass

    def save(self, directory: str) -> str:
        os.makedirs(directory, exist_ok=True)
        filename = f"{self.model_name.lower()}_{self.version}.joblib"
        filepath = os.path.join(directory, filename)
        joblib.dump(self, filepath)
        print(f"Saved {self.model_name} artifact to {filepath}")
        return filepath

    @classmethod
    def load(cls, filepath: str) -> "BaseHealthRiskModel":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model artifact not found at {filepath}")
        return joblib.load(filepath)
