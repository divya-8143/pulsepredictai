import numpy as np
import pandas as pd
from typing import Dict, Any, List
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline

from ml_engine.models.base_model import BaseHealthRiskModel
from ml_engine.pipelines.preprocessing import build_preprocessing_pipeline

class XGBoostRiskModel(BaseHealthRiskModel):
    """
    Extreme Gradient Boosted Decision Trees with multi:softprob objective.
    """
    def __init__(
        self,
        version: str = "v1.0.0",
        n_estimators: int = 300,
        learning_rate: float = 0.05,
        max_depth: int = 6,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8,
        reg_alpha: float = 0.1,
        reg_lambda: float = 1.0
    ):
        super().__init__(model_name="XGBoost", version=version)
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.pipeline: Pipeline = None

    def fit(self, X: pd.DataFrame, y: np.ndarray, **kwargs) -> "XGBoostRiskModel":
        preprocessor = build_preprocessing_pipeline()
        classifier = XGBClassifier(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            subsample=self.subsample,
            colsample_bytree=self.colsample_bytree,
            reg_alpha=self.reg_alpha,
            reg_lambda=self.reg_lambda,
            objective="multi:softprob",
            eval_metric="mlogloss",
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
