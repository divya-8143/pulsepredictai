from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class DoctorProfile(Base, TimestampMixin):
    __tablename__ = "doctor_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    license_number = Column(String(100), unique=True, nullable=False, index=True)
    specialization = Column(String(150), nullable=False, default="Cardiology & Internal Medicine")
    hospital_affiliation = Column(String(255), nullable=False, default="PulsePredict General Hospital")
    is_approved = Column(Boolean, default=True, nullable=False)
    verification_documents = Column(JSONB, default=dict, nullable=False)

    # Relationships
    user = relationship("User", back_populates="doctor_profile")
    reviews = relationship("ClinicalReview", back_populates="doctor")
