import numpy as np
import pandas as pd
from typing import Dict, Any
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from ml_engine.models.base_model import BaseHealthRiskModel
from ml_engine.pipelines.preprocessing import build_preprocessing_pipeline

class LogisticRegressionRiskModel(BaseHealthRiskModel):
    """
    Regularized Multinomial Logistic Regression Model with calibrated probabilities.
    """
    def __init__(self, version: str = "v1.0.0", C: float = 1.0, penalty: str = "l2"):
        super().__init__(model_name="LogisticRegression", version=version)
        self.C = C
        self.penalty = penalty
        self.pipeline: Pipeline = None

    def fit(self, X: pd.DataFrame, y: np.ndarray, **kwargs) -> "LogisticRegressionRiskModel":
        preprocessor = build_preprocessing_pipeline()
        classifier = LogisticRegression(
            C=self.C,
            penalty=self.penalty,
            solver="lbfgs",
            max_iter=1000,
            multi_class="multinomial",
            random_state=42
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
        # Average absolute magnitude across multinomial classes
        avg_weights = np.mean(np.abs(classifier.coef_), axis=0)
        return {f"feature_{i}": float(w) for i, w in enumerate(avg_weights)}
