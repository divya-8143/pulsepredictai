import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import require_doctor
from app.models.user import User
from app.models.enums import RiskCategory
from app.schemas.clinical_review import (
    DoctorDashboardSummary, DoctorPatientListItem,
    ClinicalReviewCreate, ClinicalReviewResponse
)
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctor", tags=["Physician Clinical Review & Dashboard"])

@router.get("/dashboard", response_model=DoctorDashboardSummary)
async def get_doctor_dashboard_stats(
    current_user: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db)
):
    """Physician summary stats, high risk patient alerts, and review queue."""
    return await DoctorService.get_dashboard_summary(db, current_user)

@router.get("/patients", response_model=List[DoctorPatientListItem])
async def get_doctor_patient_roster(
    risk_category: Optional[RiskCategory] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db)
):
    """Query all patient profiles with multi-tier risk filtering and full search."""
    return await DoctorService.get_patient_roster(db, risk_category, search, page, page_size)

@router.post("/reviews", response_model=ClinicalReviewResponse, status_code=status.HTTP_201_CREATED)
async def submit_clinical_review(
    data: ClinicalReviewCreate,
    current_user: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db)
):
    """Physician submit clinical review annotations and follow-up directives."""
    return await DoctorService.submit_review(db, current_user, data)
