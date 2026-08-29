import uuid
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.assessment import HealthAssessment
from app.models.patient import PatientProfile
from app.models.enums import UserRole
from app.services.pdf_service import ClinicalPDFReportService
from app.core.exceptions import EntityNotFoundException, ForbiddenException

router = APIRouter(prefix="/reports", tags=["Clinical PDF Report Generation"])

@router.get("/assessment/{assessment_id}/pdf")
async def download_assessment_pdf(
    assessment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate and download clinical-grade PDF assessment report.
    """
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

    # Authorization
    if current_user.role == UserRole.PATIENT and assessment.patient.user_id != current_user.id:
        raise ForbiddenException("Cannot access another patient's medical PDF report.")

    doctor_review = assessment.reviews[0] if assessment.reviews else None
    pdf_buffer = ClinicalPDFReportService.generate_assessment_pdf(
        assessment, assessment.patient, doctor_review
    )

    filename = f"PulsePredict_Clinical_Report_{str(assessment_id)[:8]}.pdf"
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
