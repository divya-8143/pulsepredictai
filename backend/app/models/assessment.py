from sqlalchemy import Column, Float, Boolean, String, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.enums import SmokingStatus, AlcoholConsumption, RiskCategory

class HealthAssessment(Base, TimestampMixin):
    __tablename__ = "health_assessments"

    patient_id = Column(UUID(as_uuid=True), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Biometrics & Laboratory Metrics
    age = Column(Float, nullable=False)
    systolic_bp = Column(Float, nullable=False)
    diastolic_bp = Column(Float, nullable=False)
    resting_heart_rate = Column(Float, default=72.0, nullable=False)
    total_cholesterol = Column(Float, nullable=False)
    hdl_cholesterol = Column(Float, nullable=False)
    ldl_cholesterol = Column(Float, nullable=False)
    triglycerides = Column(Float, default=150.0, nullable=False)
    bmi = Column(Float, nullable=False)
    fasting_glucose = Column(Float, nullable=False)
    hba1c = Column(Float, default=5.6, nullable=False)
    
    # Lifestyle & Genetic Features
    smoking_status = Column(SQLEnum(SmokingStatus), default=SmokingStatus.NEVER, nullable=False)
    alcohol_consumption = Column(SQLEnum(AlcoholConsumption), default=AlcoholConsumption.NONE, nullable=False)
    physical_activity_hours_week = Column(Float, default=2.5, nullable=False)
    family_history_cad = Column(Boolean, default=False, nullable=False)
    family_history_diabetes = Column(Boolean, default=False, nullable=False)
    family_history_hypertension = Column(Boolean, default=False, nullable=False)
    
    # ML Prediction Outputs
    overall_risk_score = Column(Float, nullable=False, index=True)  # 0.0 - 100.0
    risk_category = Column(SQLEnum(RiskCategory), nullable=False, index=True)
    primary_model_name = Column(String(100), default="Ensemble (LR+RF+XGB)", nullable=False)
    ensemble_predictions = Column(JSONB, default=dict, nullable=False)  # Breakdown by individual model
    feature_importance_shap = Column(JSONB, default=dict, nullable=False)  # Localized SHAP contributions
    assessed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    patient = relationship("PatientProfile", back_populates="assessments")
    reviews = relationship("ClinicalReview", back_populates="assessment", cascade="all, delete-orphan")
