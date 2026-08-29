import uuid
from datetime import datetime
from app.models.assessment import HealthAssessment
from app.models.patient import PatientProfile
from app.models.user import User
from app.models.enums import SmokingStatus, AlcoholConsumption, RiskCategory, Gender
from app.services.pdf_service import ClinicalPDFReportService

def test_clinical_pdf_report_generation():
    fake_user = User(
        id=uuid.uuid4(),
        email="test.patient@pulsepredict.ai",
        full_name="Test Patient Emily",
        hashed_password="hash",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    fake_patient = PatientProfile(
        id=uuid.uuid4(),
        user_id=fake_user.id,
        gender=Gender.FEMALE,
        blood_group="B+",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    fake_patient.user = fake_user

    fake_assessment = HealthAssessment(
        id=uuid.uuid4(),
        patient_id=fake_patient.id,
        age=52.0,
        systolic_bp=138.0,
        diastolic_bp=88.0,
        resting_heart_rate=74.0,
        total_cholesterol=220.0,
        hdl_cholesterol=45.0,
        ldl_cholesterol=140.0,
        triglycerides=170.0,
        bmi=27.5,
        fasting_glucose=105.0,
        hba1c=5.8,
        smoking_status=SmokingStatus.NEVER,
        alcohol_consumption=AlcoholConsumption.NONE,
        physical_activity_hours_week=2.5,
        family_history_cad=False,
        family_history_diabetes=False,
        family_history_hypertension=False,
        overall_risk_score=42.5,
        risk_category=RiskCategory.MODERATE,
        primary_model_name="Calibrated Ensemble (LR + RF + XGBoost)",
        ensemble_predictions={},
        feature_importance_shap=[
            {"feature_name": "systolic_bp", "display_name": "Systolic Blood Pressure", "feature_value": 138, "shap_value": 0.12, "impact": "INCREASES_RISK", "clinical_note": "Stage 1 Hypertension"}
        ],
        assessed_at=datetime.utcnow()
    )

    pdf_buffer = ClinicalPDFReportService.generate_assessment_pdf(fake_assessment, fake_patient)
    pdf_bytes = pdf_buffer.getvalue()

    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF-")
