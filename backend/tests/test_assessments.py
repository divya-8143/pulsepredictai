import pytest
from pydantic import ValidationError
from app.schemas.assessment import HealthDataInput
from app.services.validation_service import BiomarkerValidationService
from app.core.exceptions import ValidationException
from app.models.enums import SmokingStatus, AlcoholConsumption

def test_valid_health_data_input():
    data = HealthDataInput(
        age=45.0,
        systolic_bp=125.0,
        diastolic_bp=80.0,
        resting_heart_rate=72.0,
        total_cholesterol=195.0,
        hdl_cholesterol=50.0,
        ldl_cholesterol=115.0,
        triglycerides=150.0,
        bmi=24.5,
        fasting_glucose=92.0,
        hba1c=5.3,
        smoking_status=SmokingStatus.NEVER,
        alcohol_consumption=AlcoholConsumption.NONE,
        physical_activity_hours_week=3.0,
        family_history_cad=False,
        family_history_diabetes=False,
        family_history_hypertension=False
    )
    assert data.age == 45.0
    BiomarkerValidationService.validate_physiological_coherence(data)

def test_invalid_blood_pressure_diastolic_greater():
    with pytest.raises(ValidationError):
        HealthDataInput(
            age=45.0,
            systolic_bp=110.0,
            diastolic_bp=120.0,  # Invalid: Diastolic > Systolic
            resting_heart_rate=72.0,
            total_cholesterol=195.0,
            hdl_cholesterol=50.0,
            ldl_cholesterol=115.0,
            triglycerides=150.0,
            bmi=24.5,
            fasting_glucose=92.0,
            hba1c=5.3,
            smoking_status=SmokingStatus.NEVER,
            alcohol_consumption=AlcoholConsumption.NONE,
            physical_activity_hours_week=3.0,
            family_history_cad=False,
            family_history_diabetes=False,
            family_history_hypertension=False
        )
