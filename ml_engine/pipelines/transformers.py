import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class ClinicalFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Derive domain-specific physiological ratios and interaction terms:
    - Pulse Pressure = SBP - DBP
    - Cholesterol Ratio = Total Cholesterol / HDL
    - Triglyceride to HDL Ratio (Atherogenic index)
    - Mean Arterial Pressure (MAP) = DBP + 1/3(SBP - DBP)
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        if isinstance(df, np.ndarray):
            # If array passed, return as is
            return df
        
        df["pulse_pressure"] = df["systolic_bp"] - df["diastolic_bp"]
        df["cholesterol_ratio"] = df["total_cholesterol"] / np.clip(df["hdl_cholesterol"], 1.0, None)
        df["tg_to_hdl_ratio"] = df["triglycerides"] / np.clip(df["hdl_cholesterol"], 1.0, None)
        df["mean_arterial_pressure"] = df["diastolic_bp"] + (1.0 / 3.0) * df["pulse_pressure"]
        
        return df
