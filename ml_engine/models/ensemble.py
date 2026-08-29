import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from ml_engine.models.base_model import BaseHealthRiskModel
from ml_engine.models.logistic_regression import LogisticRegressionRiskModel
from ml_engine.models.random_forest import RandomForestRiskModel
from ml_engine.models.xgboost_model import XGBoostRiskModel

class CalibratedEnsembleRiskModel(BaseHealthRiskModel):
    """
    Calibrated Soft-Voting Clinical Ensemble blending Logistic Regression, Random Forest, and XGBoost.
    """
    def __init__(
        self,
        models: Dict[str, BaseHealthRiskModel],
        weights: Dict[str, float] = None,
        version: str = "v1.0.0"
    ):
        super().__init__(model_name="CalibratedEnsemble", version=version)
        self.models = models
        self.weights = weights or {"LogisticRegression": 0.20, "RandomForest": 0.35, "XGBoost": 0.45}
        self.is_fitted = True

    def fit(self, X: pd.DataFrame, y: np.ndarray, **kwargs):
        for name, m in self.models.items():
            m.fit(X, y)
        self.is_fitted = True
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        weighted_probs = None
        total_weight = sum(self.weights.values())

        for name, model in self.models.items():
            w = self.weights.get(name, 1.0)
            p = model.predict_proba(X)
            if weighted_probs is None:
                weighted_probs = p * w
            else:
                weighted_probs += p * w

        return weighted_probs / total_weight

    def predict_detailed_breakdown(self, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Compute overall ensemble score + individual model sub-predictions.
        """
        overall_score = float(self.predict_risk_score(X)[0])
        overall_category = self.predict_category(X)[0]
        
        breakdown = {}
        for name, model in self.models.items():
            score = float(model.predict_risk_score(X)[0])
            cat = model.predict_category(X)[0]
            prob = float(np.max(model.predict_proba(X)[0]))
            breakdown[name] = {
                "risk_score": np.round(score, 1),
                "risk_category": cat,
                "confidence_probability": np.round(prob, 4),
                "weight_in_ensemble": self.weights.get(name, 0.33)
            }

        return {
            "overall_risk_score": np.round(overall_score, 1),
            "overall_risk_category": overall_category,
            "models": breakdown
        }

    def get_feature_importances(self) -> Dict[str, float]:
        if "XGBoost" in self.models:
            return self.models["XGBoost"].get_feature_importances()
        elif "RandomForest" in self.models:
            return self.models["RandomForest"].get_feature_importances()
        return {}
