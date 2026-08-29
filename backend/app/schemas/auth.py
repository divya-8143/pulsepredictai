from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.enums import UserRole

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="Minimum 8 characters")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = Field(default=UserRole.PATIENT)
    license_number: Optional[str] = Field(default=None, description="Required for Doctor role")
    specialization: Optional[str] = Field(default=None, description="Specialization if Doctor")
    hospital_affiliation: Optional[str] = Field(default=None, description="Hospital if Doctor")

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    email: str
    full_name: str
    role: UserRole

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
