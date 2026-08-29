import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, require_doctor
from app.models.user import User
from app.schemas.patient import PatientProfileResponse, PatientProfileUpdate
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patient Profiles"])

@router.get("/me", response_model=PatientProfileResponse)
async def get_my_patient_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve demographic and baseline health profile for authenticated patient."""
    return await PatientService.get_patient_by_user_id(db, current_user.id)

@router.put("/me", response_model=PatientProfileResponse)
async def update_my_patient_profile(
    update_data: PatientProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update demographic vitals, emergency contacts, and medical history flags."""
    return await PatientService.update_patient_profile(db, current_user.id, update_data)

@router.get("/{patient_id}", response_model=PatientProfileResponse)
async def get_patient_by_id_clinical(
    patient_id: uuid.UUID,
    doctor_user: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db)
):
    """Doctor / Clinical staff access to specific patient profile by ID."""
    return await PatientService.get_patient_by_id(db, patient_id)
