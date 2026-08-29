import uuid
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.enums import ReviewRecommendation, RiskCategory

class ClinicalReviewCreate(BaseModel):
    assessment_id: uuid.UUID
    clinical_notes: str = Field(..., min_length=10, max_length=5000)
    recommendation: ReviewRecommendation = Field(default=ReviewRecommendation.LIFESTYLE_MOD)
    requires_followup: bool = Field(default=False)
    follow_up_date: Optional[date] = None

class ClinicalReviewResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    doctor_id: uuid.UUID
    doctor_name: str
    specialization: str
    clinical_notes: str
    recommendation: ReviewRecommendation
    requires_followup: bool
    follow_up_date: Optional[date] = None
    reviewed_at: datetime

    class Config:
        from_attributes = True

class DoctorPatientListItem(BaseModel):
    patient_id: uuid.UUID
    user_id: uuid.UUID
    full_name: str
    email: str
    age: Optional[float] = None
    gender: Optional[str] = None
    latest_risk_score: Optional[float] = None
    latest_risk_category: Optional[RiskCategory] = None
    latest_assessed_at: Optional[datetime] = None
    has_pending_review: bool = False

class DoctorDashboardSummary(BaseModel):
    total_patients: int
    critical_risk_count: int
    high_risk_count: int
    moderate_risk_count: int
    low_risk_count: int
    pending_reviews_count: int
    recent_critical_patients: List[DoctorPatientListItem]
