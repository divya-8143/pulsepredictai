import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.impute import SimpleImputer

from ml_engine.config import (
    NUMERICAL_FEATURES, CATEGORICAL_FEATURES, 
    BINARY_FEATURES, SAVED_MODELS_DIR
)
from ml_engine.pipelines.transformers import ClinicalFeatureEngineer

def build_preprocessing_pipeline() -> Pipeline:
    """
    Construct reproducible, production-ready scikit-learn preprocessing pipeline.
    """
    numerical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    binary_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value=0))
    ])

    # Extra numerical derived features
    engineered_numerical = [
        "age", "systolic_bp", "diastolic_bp", "resting_heart_rate",
        "total_cholesterol", "hdl_cholesterol", "ldl_cholesterol", "triglycerides",
        "bmi", "fasting_glucose", "hba1c", "physical_activity_hours_week",
        "pulse_pressure", "cholesterol_ratio", "tg_to_hdl_ratio", "mean_arterial_pressure"
    ]

    col_transformer = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, engineered_numerical),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
            ("bin", binary_transformer, BINARY_FEATURES),
        ],
        remainder="drop"
    )

    full_pipeline = Pipeline(steps=[
        ("feature_engineering", ClinicalFeatureEngineer()),
        ("preprocessor", col_transformer)
    ])

    return full_pipeline

def save_pipeline(pipeline: Pipeline, filename: str = "preprocessor_pipeline.joblib") -> str:
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    save_path = os.path.join(SAVED_MODELS_DIR, filename)
    joblib.dump(pipeline, save_path)
    print(f"Saved preprocessor pipeline to {save_path}")
    return save_path

def load_pipeline(filename: str = "preprocessor_pipeline.joblib") -> Pipeline:
    path = os.path.join(SAVED_MODELS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Preprocessor pipeline artifact not found at {path}")
    return joblib.load(path)
