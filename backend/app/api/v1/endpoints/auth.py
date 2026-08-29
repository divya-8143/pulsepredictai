from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import (
    UserRegisterRequest, UserLoginRequest, 
    TokenResponse, RefreshTokenRequest, PasswordChangeRequest
)
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User
from app.core.security import verify_password, get_password_hash
from app.core.exceptions import ValidationException

router = APIRouter(prefix="/auth", tags=["Authentication & RBAC"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new Patient or Doctor with role credentials."""
    return await AuthService.register(db, req)

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate user and issue cryptographic JWT tokens."""
    return await AuthService.login(db, req)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Refresh expired access token using valid refresh token."""
    return await AuthService.refresh_tokens(db, req)

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    req: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update password for currently authenticated user."""
    if not verify_password(req.current_password, current_user.hashed_password):
        raise ValidationException("Current password verification failed.")
    
    current_user.hashed_password = get_password_hash(req.new_password)
    db.add(current_user)
    await db.commit()
    return {"message": "Password updated successfully."}
