import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from ml_engine.models.base_model import BaseHealthRiskModel
from ml_engine.pipelines.preprocessing import build_preprocessing_pipeline

class RandomForestRiskModel(BaseHealthRiskModel):
    """
    Clinical Random Forest Ensemble with cost-complexity pruning and feature importance tracking.
    """
    def __init__(
        self,
        version: str = "v1.0.0",
        n_estimators: int = 250,
        max_depth: int = 12,
        min_samples_split: int = 5,
        min_samples_leaf: int = 2
    ):
        super().__init__(model_name="RandomForest", version=version)
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.pipeline: Pipeline = None

    def fit(self, X: pd.DataFrame, y: np.ndarray, **kwargs) -> "RandomForestRiskModel":
        preprocessor = build_preprocessing_pipeline()
        classifier = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            criterion="gini",
            random_state=42,
            n_jobs=-1
        )
        self.pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier)
        ])
        self.pipeline.fit(X, y)
        self.is_fitted = True
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.pipeline is None:
            raise RuntimeError("Model is not fitted.")
        return self.pipeline.predict_proba(X)

    def get_feature_importances(self) -> Dict[str, float]:
        if not self.is_fitted or self.pipeline is None:
            return {}
        classifier = self.pipeline.named_steps["classifier"]
        importances = classifier.feature_importances_
        return {f"feature_{i}": float(imp) for i, imp in enumerate(importances)}
