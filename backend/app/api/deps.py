import uuid
from typing import AsyncGenerator, Callable, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException, EntityNotFoundException
from app.models.user import User
from app.models.enums import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_token(token)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Malformed token payload.")
    
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException("Invalid user ID in token.")

    query = select(User).where(User.id == user_uuid).options(
        selectinload(User.patient_profile),
        selectinload(User.doctor_profile)
    )
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise EntityNotFoundException("User", user_id_str)
    if not user.is_active:
        raise ForbiddenException("User account is inactive or disabled.")

    return user

def require_roles(allowed_roles: List[UserRole]) -> Callable:
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                f"Access denied. Requires one of roles: {[r.value for r in allowed_roles]}."
            )
        return current_user
    return role_checker

require_patient = require_roles([UserRole.PATIENT, UserRole.ADMIN])
require_doctor = require_roles([UserRole.DOCTOR, UserRole.ADMIN])
require_admin = require_roles([UserRole.ADMIN])
