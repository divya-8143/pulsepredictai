from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserResponse, UserProfileResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["User Profile & Management"])

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Retrieve profile details of the authenticated user."""
    profile_data = {}
    patient_id = None
    doctor_id = None

    if current_user.patient_profile:
        patient_id = current_user.patient_profile.id
        profile_data = {
            "date_of_birth": str(current_user.patient_profile.date_of_birth) if current_user.patient_profile.date_of_birth else None,
            "gender": current_user.patient_profile.gender,
            "blood_group": current_user.patient_profile.blood_group,
            "phone_number": current_user.patient_profile.phone_number,
            "emergency_contact": current_user.patient_profile.emergency_contact,
            "medical_history_flags": current_user.patient_profile.medical_history_flags
        }
    elif current_user.doctor_profile:
        doctor_id = current_user.doctor_profile.id
        profile_data = {
            "license_number": current_user.doctor_profile.license_number,
            "specialization": current_user.doctor_profile.specialization,
            "hospital_affiliation": current_user.doctor_profile.hospital_affiliation,
            "is_approved": current_user.doctor_profile.is_approved
        }

    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        patient_profile_id=patient_id,
        doctor_profile_id=doctor_id,
        profile_data=profile_data
    )

@router.get("", response_model=List[UserResponse])
async def list_all_users(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Administrator endpoint to list all registered system users."""
    stmt = select(User).order_by(User.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()
