import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, require_patient, require_doctor
from app.models.user import User
from app.models.enums import RiskCategory
from app.schemas.assessment import (
    HealthDataInput, RiskAssessmentResponse, 
    PaginatedAssessmentHistory
)
from app.services.assessment_service import AssessmentService

router = APIRouter(prefix="/assessments", tags=["Health Risk Assessments"])

@router.post("/predict", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    data: HealthDataInput,
    target_patient_id: Optional[uuid.UUID] = Query(None, description="Patient UUID if submitted by Doctor"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest patient health biomarkers, run multi-model ML risk assessment, and persist results.
    """
    return await AssessmentService.create_assessment(db, current_user, data, target_patient_id)

@router.get("/history", response_model=PaginatedAssessmentHistory)
async def get_my_assessment_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    risk_category: Optional[RiskCategory] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve paginated assessment history for currently authenticated patient."""
    if not current_user.patient_profile:
        return PaginatedAssessmentHistory(items=[], total=0, page=page, page_size=page_size, total_pages=1)
    
    return await AssessmentService.get_patient_history(
        db, current_user.patient_profile.id, page, page_size, risk_category
    )

@router.get("/trends", response_model=List[Dict[str, Any]])
async def get_my_longitudinal_trends(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve time-series biomarker trends and risk trajectory for authenticated patient."""
    if not current_user.patient_profile:
        return []
    return await AssessmentService.get_longitudinal_trends(db, current_user.patient_profile.id)

@router.get("/{assessment_id}", response_model=RiskAssessmentResponse)
async def get_assessment_details(
    assessment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve full assessment details including SHAP feature attribution breakdown."""
    return await AssessmentService.get_assessment_by_id(db, current_user, assessment_id)
