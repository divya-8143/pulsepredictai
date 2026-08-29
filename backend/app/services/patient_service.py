import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.patient import PatientProfile
from app.models.user import User
from app.schemas.patient import PatientProfileUpdate, PatientProfileResponse
from app.core.exceptions import EntityNotFoundException, ValidationException

class PatientService:
    @staticmethod
    async def get_patient_by_user_id(db: AsyncSession, user_id: uuid.UUID) -> PatientProfileResponse:
        stmt = (
            select(PatientProfile)
            .join(PatientProfile.user)
            .where(PatientProfile.user_id == user_id)
            .options(selectinload(PatientProfile.user))
        )
        res = await db.execute(stmt)
        profile = res.scalars().first()
        if not profile:
            raise EntityNotFoundException("PatientProfile", user_id)

        return PatientProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            full_name=profile.user.full_name,
            email=profile.user.email,
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            blood_group=profile.blood_group,
            phone_number=profile.phone_number,
            emergency_contact=profile.emergency_contact,
            medical_history_flags=profile.medical_history_flags or {},
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

    @staticmethod
    async def get_patient_by_id(db: AsyncSession, patient_id: uuid.UUID) -> PatientProfileResponse:
        stmt = (
            select(PatientProfile)
            .join(PatientProfile.user)
            .where(PatientProfile.id == patient_id)
            .options(selectinload(PatientProfile.user))
        )
        res = await db.execute(stmt)
        profile = res.scalars().first()
        if not profile:
            raise EntityNotFoundException("PatientProfile", patient_id)

        return PatientProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            full_name=profile.user.full_name,
            email=profile.user.email,
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            blood_group=profile.blood_group,
            phone_number=profile.phone_number,
            emergency_contact=profile.emergency_contact,
            medical_history_flags=profile.medical_history_flags or {},
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

    @staticmethod
    async def update_patient_profile(
        db: AsyncSession, user_id: uuid.UUID, update_data: PatientProfileUpdate
    ) -> PatientProfileResponse:
        stmt = (
            select(PatientProfile)
            .join(PatientProfile.user)
            .where(PatientProfile.user_id == user_id)
            .options(selectinload(PatientProfile.user))
        )
        res = await db.execute(stmt)
        profile = res.scalars().first()
        if not profile:
            # Create if not exists
            profile = PatientProfile(user_id=user_id, medical_history_flags={})
            db.add(profile)
            await db.flush()

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(profile, key, value)

        db.add(profile)
        await db.commit()
        await db.refresh(profile)

        return PatientProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            full_name=profile.user.full_name,
            email=profile.user.email,
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            blood_group=profile.blood_group,
            phone_number=profile.phone_number,
            emergency_contact=profile.emergency_contact,
            medical_history_flags=profile.medical_history_flags or {},
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
