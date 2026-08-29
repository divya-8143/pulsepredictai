from sqlalchemy import Column, Date, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.enums import Gender

class PatientProfile(Base, TimestampMixin):
    __tablename__ = "patient_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(SQLEnum(Gender), default=Gender.OTHER, nullable=True)
    blood_group = Column(String(10), nullable=True)
    phone_number = Column(String(30), nullable=True)
    emergency_contact = Column(String(255), nullable=True)
    medical_history_flags = Column(JSONB, default=dict, nullable=False)

    # Relationships
    user = relationship("User", back_populates="patient_profile")
    assessments = relationship("HealthAssessment", back_populates="patient", cascade="all, delete-orphan")
