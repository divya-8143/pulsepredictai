import pytest
import numpy as np
import pandas as pd
from ml_engine.models.logistic_regression import LogisticRegressionRiskModel
from ml_engine.models.random_forest import RandomForestRiskModel
from ml_engine.models.xgboost_model import XGBoostRiskModel
from ml_engine.models.ensemble import CalibratedEnsembleRiskModel

@pytest.fixture
def sample_clinical_data():
    df = pd.DataFrame([{
        "age": 50.0,
        "systolic_bp": 130.0,
        "diastolic_bp": 85.0,
        "resting_heart_rate": 72.0,
        "total_cholesterol": 200.0,
        "hdl_cholesterol": 50.0,
        "ldl_cholesterol": 120.0,
        "triglycerides": 150.0,
        "bmi": 25.0,
        "fasting_glucose": 95.0,
        "hba1c": 5.5,
        "smoking_status": "NEVER",
        "alcohol_consumption": "NONE",
        "physical_activity_hours_week": 3.0,
        "family_history_cad": 0.0,
        "family_history_diabetes": 0.0,
        "family_history_hypertension": 0.0,
    }])
    return df

def test_model_inference_shapes(sample_clinical_data):
    from ml_engine.training.registry import ModelRegistryService
    registry = ModelRegistryService.get_instance()
    ensemble = registry.get_ensemble()

    breakdown = ensemble.predict_detailed_breakdown(sample_clinical_data)
    assert "overall_risk_score" in breakdown
    assert 0.0 <= breakdown["overall_risk_score"] <= 100.0
    assert breakdown["overall_risk_category"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]
