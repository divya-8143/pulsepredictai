import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from app.models.enums import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool = True
    is_verified: bool = False

class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserProfileResponse(UserResponse):
    patient_profile_id: Optional[uuid.UUID] = None
    doctor_profile_id: Optional[uuid.UUID] = None
    profile_data: Optional[Dict[str, Any]] = None
