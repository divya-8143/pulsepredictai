from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, GUID

class DoctorProfile(Base, TimestampMixin):
    __tablename__ = "doctor_profiles"

    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    license_number = Column(String(100), unique=True, nullable=False, index=True)
    specialization = Column(String(150), nullable=False, default="Cardiology & Internal Medicine")
    hospital_affiliation = Column(String(255), nullable=False, default="PulsePredict General Hospital")
    is_approved = Column(Boolean, default=True, nullable=False)
    verification_documents = Column(JSON, default=dict, nullable=False)

    user = relationship("User", back_populates="doctor_profile")
    reviews = relationship("ClinicalReview", back_populates="doctor")
