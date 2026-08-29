from sqlalchemy import Column, Text, Boolean, Date, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models.base import TimestampMixin, GUID
from app.models.enums import ReviewRecommendation

class ClinicalReview(Base, TimestampMixin):
    __tablename__ = "clinical_reviews"

    assessment_id = Column(GUID(), ForeignKey("health_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = Column(GUID(), ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    clinical_notes = Column(Text, nullable=False)
    recommendation = Column(SQLEnum(ReviewRecommendation), default=ReviewRecommendation.LIFESTYLE_MOD, nullable=False)
    requires_followup = Column(Boolean, default=False, nullable=False)
    follow_up_date = Column(Date, nullable=True)
    reviewed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    assessment = relationship("HealthAssessment", back_populates="reviews")
    doctor = relationship("DoctorProfile", back_populates="reviews")
