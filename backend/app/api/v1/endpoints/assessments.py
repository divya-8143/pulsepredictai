import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.enums import RiskCategory, UserRole
from app.models.assessment import HealthAssessment
from app.models.patient import PatientProfile
from app.schemas.assessment import (
    HealthDataInput, RiskAssessmentResponse, 
    PaginatedAssessmentHistory
)
from app.services.assessment_service import AssessmentService
from app.services.dietary_engine import PersonalizedDietaryEngine
from app.services.pdf_service import ClinicalPDFReportService
from app.core.exceptions import EntityNotFoundException, ForbiddenException

router = APIRouter(prefix="/assessments", tags=["Health Risk Assessments"])

@router.post("/predict", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    data: HealthDataInput,
    target_patient_id: Optional[uuid.UUID] = Query(None, description="Patient UUID if submitted by Doctor"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Ingest patient biomarkers, execute ML risk ensemble, and persist assessment."""
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
    """Retrieve longitudinal biomarker trajectory for authenticated patient."""
    if not current_user.patient_profile:
        return []
    return await AssessmentService.get_longitudinal_trends(db, current_user.patient_profile.id)

@router.get("/{assessment_id}", response_model=RiskAssessmentResponse)
async def get_assessment_details(
    assessment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve full assessment details with SHAP feature attribution breakdown."""
    return await AssessmentService.get_assessment_by_id(db, current_user, assessment_id)

@router.get("/{assessment_id}/report")
async def download_patient_assessment_report(
    assessment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download official clinical PDF assessment report for patient or physician."""
    stmt = (
        select(HealthAssessment)
        .where(HealthAssessment.id == assessment_id)
        .options(
            selectinload(HealthAssessment.patient).selectinload(PatientProfile.user),
            selectinload(HealthAssessment.reviews)
        )
    )
    res = await db.execute(stmt)
    assessment = res.scalars().first()
    if not assessment:
        raise EntityNotFoundException("HealthAssessment", assessment_id)

    if current_user.role == UserRole.PATIENT and assessment.patient.user_id != current_user.id:
        raise ForbiddenException("Cannot access another patient's medical report.")

    doctor_review = assessment.reviews[0] if assessment.reviews else None
    pdf_buffer = ClinicalPDFReportService.generate_assessment_pdf(
        assessment, assessment.patient, doctor_review
    )

    filename = f"PulsePredict_Report_{str(assessment_id)[:8]}.pdf"
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.get("/{assessment_id}/diet-plan")
async def get_assessment_diet_plan(
    assessment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve customized cardiorespiratory & metabolic balanced diet plan for an assessment."""
    stmt = (
        select(HealthAssessment)
        .where(HealthAssessment.id == assessment_id)
        .options(selectinload(HealthAssessment.patient))
    )
    res = await db.execute(stmt)
    assessment = res.scalars().first()
    if not assessment:
        raise EntityNotFoundException("HealthAssessment", assessment_id)

    if current_user.role == UserRole.PATIENT and assessment.patient.user_id != current_user.id:
        raise ForbiddenException("Cannot access another patient's diet plan.")

    biomarkers = {
        "age": assessment.age,
        "gender": assessment.patient.gender if assessment.patient else "MALE",
        "bmi": assessment.bmi,
        "systolic_bp": assessment.systolic_bp,
        "diastolic_bp": assessment.diastolic_bp,
        "fasting_glucose": assessment.fasting_glucose,
        "hba1c": assessment.hba1c,
        "total_cholesterol": assessment.total_cholesterol,
        "ldl_cholesterol": assessment.ldl_cholesterol,
        "triglycerides": assessment.triglycerides,
        "physical_activity_hours_week": assessment.physical_activity_hours_week
    }

    diet_plan = PersonalizedDietaryEngine.generate_diet_plan(
        biomarkers, str(assessment.risk_category.value if hasattr(assessment.risk_category, "value") else assessment.risk_category)
    )
    return diet_plan
