import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.patient import PatientProfile
from app.models.doctor import DoctorProfile
from app.models.enums import UserRole
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, RefreshTokenRequest
from app.core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token, decode_token
)
from app.core.exceptions import ValidationException, UnauthorizedException
from app.core.config import settings

class AuthService:
    @staticmethod
    async def register(db: AsyncSession, req: UserRegisterRequest) -> TokenResponse:
        # Check existing user
        stmt = select(User).where(User.email == req.email.lower())
        res = await db.execute(stmt)
        if res.scalars().first():
            raise ValidationException(f"User with email '{req.email}' already exists.")

        if req.role == UserRole.DOCTOR and not req.license_number:
            raise ValidationException("Doctor registration requires a valid medical license number.")

        hashed_pw = get_password_hash(req.password)
        new_user = User(
            email=req.email.lower(),
            hashed_password=hashed_pw,
            full_name=req.full_name,
            role=req.role,
            is_active=True,
            is_verified=True
        )
        db.add(new_user)
        await db.flush()

        # Create corresponding profile
        if req.role == UserRole.PATIENT or req.role == UserRole.ADMIN:
            profile = PatientProfile(
                user_id=new_user.id,
                medical_history_flags={}
            )
            db.add(profile)
        elif req.role == UserRole.DOCTOR:
            doctor_profile = DoctorProfile(
                user_id=new_user.id,
                license_number=req.license_number,
                specialization=req.specialization or "Cardiology & Internal Medicine",
                hospital_affiliation=req.hospital_affiliation or "PulsePredict General Hospital",
                is_approved=True,
                verification_documents={}
            )
            db.add(doctor_profile)

        await db.commit()
        await db.refresh(new_user)

        access_token = create_access_token(new_user.id, new_user.role.value)
        refresh_token = create_refresh_token(new_user.id, new_user.role.value)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=str(new_user.id),
            email=new_user.email,
            full_name=new_user.full_name,
            role=new_user.role
        )

    @staticmethod
    async def login(db: AsyncSession, req: UserLoginRequest) -> TokenResponse:
        stmt = select(User).where(User.email == req.email.lower())
        res = await db.execute(stmt)
        user = res.scalars().first()

        if not user or not verify_password(req.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")
        if not user.is_active:
            raise UnauthorizedException("User account is inactive. Please contact support.")

        access_token = create_access_token(user.id, user.role.value)
        refresh_token = create_refresh_token(user.id, user.role.value)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role
        )

    @staticmethod
    async def refresh_tokens(db: AsyncSession, req: RefreshTokenRequest) -> TokenResponse:
        payload = decode_token(req.refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Provided token is not a refresh token.")

        user_id_str = payload.get("sub")
        stmt = select(User).where(User.id == uuid.UUID(user_id_str))
        res = await db.execute(stmt)
        user = res.scalars().first()

        if not user or not user.is_active:
            raise UnauthorizedException("Invalid user session.")

        access_token = create_access_token(user.id, user.role.value)
        refresh_token = create_refresh_token(user.id, user.role.value)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role
        )
