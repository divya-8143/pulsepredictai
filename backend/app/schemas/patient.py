import uuid
from datetime import date, datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.enums import Gender

class PatientProfileBase(BaseModel):
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = Gender.OTHER
    blood_group: Optional[str] = Field(None, max_length=10)
    phone_number: Optional[str] = Field(None, max_length=30)
    emergency_contact: Optional[str] = Field(None, max_length=255)
    medical_history_flags: Dict[str, Any] = Field(default_factory=dict)

class PatientProfileCreate(PatientProfileBase):
    pass

class PatientProfileUpdate(BaseModel):
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    blood_group: Optional[str] = None
    phone_number: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history_flags: Optional[Dict[str, Any]] = None

class PatientProfileResponse(PatientProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID
    full_name: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
