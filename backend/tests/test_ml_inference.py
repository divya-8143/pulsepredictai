import pytest
import pandas as pd
from app.schemas.assessment import HealthDataInput
from app.services.ml_inference_service import MLInferenceService
from app.models.enums import SmokingStatus, AlcoholConsumption, RiskCategory

def test_ml_inference_engine_execution():
    biomarkers = HealthDataInput(
        age=56.0,
        systolic_bp=152.0,
        diastolic_bp=96.0,
        resting_heart_rate=80.0,
        total_cholesterol=255.0,
        hdl_cholesterol=38.0,
        ldl_cholesterol=175.0,
        triglycerides=210.0,
        bmi=32.4,
        fasting_glucose=142.0,
        hba1c=7.2,
        smoking_status=SmokingStatus.CURRENT,
        alcohol_consumption=AlcoholConsumption.HEAVY,
        physical_activity_hours_week=0.5,
        family_history_cad=True,
        family_history_diabetes=True,
        family_history_hypertension=True
    )

    result = MLInferenceService.run_risk_assessment(biomarkers)

    assert "overall_risk_score" in result
    assert 0.0 <= result["overall_risk_score"] <= 100.0
    assert result["risk_category"] in [RiskCategory.LOW, RiskCategory.MODERATE, RiskCategory.HIGH, RiskCategory.CRITICAL]
    assert "LogisticRegression" in result["ensemble_predictions"]
    assert "RandomForest" in result["ensemble_predictions"]
    assert "XGBoost" in result["ensemble_predictions"]
    assert len(result["feature_importance_shap"]) > 0
    assert len(result["clinical_recommendations"]) > 0
