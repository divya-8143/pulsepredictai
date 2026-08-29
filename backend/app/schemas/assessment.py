import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, field_validator
from app.models.enums import SmokingStatus, AlcoholConsumption, RiskCategory

class HealthDataInput(BaseModel):
    # Demographics
    age: float = Field(..., ge=18.0, le=105.0, description="Age in years (18-105)")
    
    # Cardiovascular Vitals
    systolic_bp: float = Field(..., ge=70.0, le=240.0, description="Systolic Blood Pressure (mmHg)")
    diastolic_bp: float = Field(..., ge=40.0, le=140.0, description="Diastolic Blood Pressure (mmHg)")
    resting_heart_rate: float = Field(default=72.0, ge=35.0, le=200.0, description="Resting Heart Rate (bpm)")
    
    # Lipid & Metabolic Panel
    total_cholesterol: float = Field(..., ge=90.0, le=450.0, description="Total Cholesterol (mg/dL)")
    hdl_cholesterol: float = Field(..., ge=15.0, le=120.0, description="HDL Cholesterol (mg/dL)")
    ldl_cholesterol: float = Field(..., ge=30.0, le=300.0, description="LDL Cholesterol (mg/dL)")
    triglycerides: float = Field(default=150.0, ge=40.0, le=600.0, description="Triglycerides (mg/dL)")
    bmi: float = Field(..., ge=12.0, le=65.0, description="Body Mass Index (kg/m²)")
    fasting_glucose: float = Field(..., ge=50.0, le=350.0, description="Fasting Blood Glucose (mg/dL)")
    hba1c: float = Field(default=5.6, ge=3.5, le=16.0, description="HbA1c Level (%)")
    
    # Lifestyle & Genetic Predispositions
    smoking_status: SmokingStatus = Field(default=SmokingStatus.NEVER)
    alcohol_consumption: AlcoholConsumption = Field(default=AlcoholConsumption.NONE)
    physical_activity_hours_week: float = Field(default=2.5, ge=0.0, le=40.0, description="Physical Activity (hours/week)")
    family_history_cad: bool = Field(default=False, description="Family history of Coronary Artery Disease")
    family_history_diabetes: bool = Field(default=False, description="Family history of Type 2 Diabetes")
    family_history_hypertension: bool = Field(default=False, description="Family history of Hypertension")

    @field_validator("diastolic_bp")
    @classmethod
    def validate_blood_pressure(cls, diastolic: float, info) -> float:
        systolic = info.data.get("systolic_bp")
        if systolic and diastolic >= systolic:
            raise ValueError(f"Diastolic BP ({diastolic}) must be strictly less than Systolic BP ({systolic}).")
        if systolic and (systolic - diastolic) < 15.0:
            raise ValueError("Pulse pressure (Systolic - Diastolic) is unrealistically low (< 15 mmHg).")
        return diastolic

class SHAPFeatureContribution(BaseModel):
    feature_name: str
    display_name: str
    feature_value: Any
    shap_value: float
    impact: str  # "INCREASES_RISK", "DECREASES_RISK", "NEUTRAL"
    clinical_note: str

class IndividualModelResult(BaseModel):
    model_name: str
    risk_probability: float  # 0.0 to 1.0
    risk_score: float        # 0.0 to 100.0
    predicted_category: RiskCategory
    confidence_interval: List[float] = []

class RiskAssessmentResponse(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    overall_risk_score: float
    risk_category: RiskCategory
    primary_model_name: str
    ensemble_predictions: Dict[str, Any]
    feature_importance_shap: List[SHAPFeatureContribution]
    clinical_recommendations: List[str]
    input_biomarkers: HealthDataInput
    assessed_at: datetime
    disclaimer: str = (
        "PulsePredict AI provides predictive health risk estimation and decision support for clinical research and preventive monitoring. "
        "It does NOT constitute a medical diagnosis. Please consult a licensed medical provider for diagnostic evaluation."
    )

    class Config:
        from_attributes = True

class AssessmentHistoryItem(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    patient_name: Optional[str] = None
    age: float
    systolic_bp: float
    diastolic_bp: float
    bmi: float
    fasting_glucose: float
    total_cholesterol: float
    overall_risk_score: float
    risk_category: RiskCategory
    assessed_at: datetime
    has_doctor_review: bool = False
    doctor_recommendation: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedAssessmentHistory(BaseModel):
    items: List[AssessmentHistoryItem]
    total: int
    page: int
    page_size: int
    total_pages: int
