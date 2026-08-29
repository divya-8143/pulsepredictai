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
    - Converts boolean flags to numeric floats for estimator compatibility.
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        if not isinstance(df, pd.DataFrame):
            return df
        
        # Calculate derived physiological features
        df["pulse_pressure"] = df["systolic_bp"] - df["diastolic_bp"]
        df["cholesterol_ratio"] = df["total_cholesterol"] / np.clip(df["hdl_cholesterol"], 1.0, None)
        df["tg_to_hdl_ratio"] = df["triglycerides"] / np.clip(df["hdl_cholesterol"], 1.0, None)
        df["mean_arterial_pressure"] = df["diastolic_bp"] + (1.0 / 3.0) * df["pulse_pressure"]
        
        # Cast boolean columns to float
        for c in ["family_history_cad", "family_history_diabetes", "family_history_hypertension"]:
            if c in df.columns:
                df[c] = df[c].astype(float)
            
        return df
