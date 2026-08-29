import pytest
from app.schemas.assessment import HealthDataInput
from app.services.anomaly_detection_service import BiomarkerAnomalyDetectionService
from app.core.cache import MultiTierInferenceCache
from ml_engine.evaluation.uncertainty_engine import BayesianUncertaintyEngine
from app.services.audit_ledger_service import CryptographicAuditLedger
from app.models.enums import SmokingStatus, AlcoholConsumption

def test_inference_cache_performance():
    cache = MultiTierInferenceCache()
    sample = {"age": 52.0, "systolic_bp": 130.0, "glucose": 100.0}
    key = cache.generate_biomarker_hash(sample)
    
    cache.set(key, {"risk_score": 45.0})
    cached = cache.get(key)
    assert cached is not None
    assert cached["risk_score"] == 45.0

def test_physiological_anomaly_detection():
    # Extreme glucose with low HbA1c (severe biochemical mismatch)
    abnormal_input = HealthDataInput(
        age=50.0, systolic_bp=135.0, diastolic_bp=85.0, resting_heart_rate=72.0,
        total_cholesterol=280.0, hdl_cholesterol=40.0, ldl_cholesterol=110.0, triglycerides=120.0,
        bmi=25.0, fasting_glucose=245.0, hba1c=4.9, smoking_status=SmokingStatus.NEVER,
        alcohol_consumption=AlcoholConsumption.NONE, physical_activity_hours_week=3.0,
        family_history_cad=False, family_history_diabetes=False, family_history_hypertension=False
    )
    report = BiomarkerAnomalyDetectionService.analyze_physiological_coherence(abnormal_input)
    assert report["discrepancy_count"] > 0
    assert len(report["discrepancies"]) > 0

def test_bayesian_uncertainty_bounds():
    profile = BayesianUncertaintyEngine.calculate_uncertainty_profile(
        biomarker_dict={"age": 55, "systolic_bp": 135},
        ensemble_model_scores={"LR": 40.0, "RF": 44.0, "XGB": 42.0},
        overall_risk_score=42.0
    )
    assert "confidence_interval_95" in profile
    assert profile["confidence_interval_95"]["lower_bound"] <= 42.0 <= profile["confidence_interval_95"]["upper_bound"]

def test_cryptographic_audit_ledger_integrity():
    CryptographicAuditLedger.record_event("ASSESSMENT", "user-1", "PATIENT", "ass-1", {"score": 42.0})
    CryptographicAuditLedger.record_event("REVIEW", "doc-1", "DOCTOR", "ass-1", {"notes": "Approved"})
    
    verification = CryptographicAuditLedger.verify_ledger_integrity()
    assert verification["is_valid"] is True
