import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc, or_
from sqlalchemy.orm import selectinload

from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.models.assessment import HealthAssessment
from app.models.clinical_review import ClinicalReview
from app.models.user import User
from app.models.enums import RiskCategory, UserRole
from app.schemas.clinical_review import (
    ClinicalReviewCreate, ClinicalReviewResponse,
    DoctorPatientListItem, DoctorDashboardSummary
)
from app.core.exceptions import EntityNotFoundException, ValidationException

class DoctorService:
    @staticmethod
    async def get_dashboard_summary(db: AsyncSession, doctor_user: User) -> DoctorDashboardSummary:
        # Total patients
        total_p_stmt = select(func.count(PatientProfile.id))
        total_patients = (await db.execute(total_p_stmt)).scalar() or 0

        # Risk categories count across latest assessments
        crit_stmt = select(func.count(HealthAssessment.id)).where(HealthAssessment.risk_category == RiskCategory.CRITICAL)
        high_stmt = select(func.count(HealthAssessment.id)).where(HealthAssessment.risk_category == RiskCategory.HIGH)
        mod_stmt = select(func.count(HealthAssessment.id)).where(HealthAssessment.risk_category == RiskCategory.MODERATE)
        low_stmt = select(func.count(HealthAssessment.id)).where(HealthAssessment.risk_category == RiskCategory.LOW)

        crit_count = (await db.execute(crit_stmt)).scalar() or 0
        high_count = (await db.execute(high_stmt)).scalar() or 0
        mod_count = (await db.execute(mod_stmt)).scalar() or 0
        low_count = (await db.execute(low_stmt)).scalar() or 0

        # Recent high / critical patients
        recent_stmt = (
            select(HealthAssessment)
            .where(HealthAssessment.risk_category.in_([RiskCategory.CRITICAL, RiskCategory.HIGH]))
            .order_by(desc(HealthAssessment.assessed_at))
            .limit(5)
            .options(selectinload(HealthAssessment.patient).selectinload(PatientProfile.user))
        )
        recent_assessments = (await db.execute(recent_stmt)).scalars().all()

        recent_items = [
            DoctorPatientListItem(
                patient_id=a.patient_id,
                user_id=a.patient.user_id,
                full_name=a.patient.user.full_name,
                email=a.patient.user.email,
                age=a.age,
                gender=a.patient.gender.value if a.patient.gender else "OTHER",
                latest_risk_score=a.overall_risk_score,
                latest_risk_category=a.risk_category,
                latest_assessed_at=a.assessed_at,
                has_pending_review=len(a.reviews) == 0
            )
            for a in recent_assessments
        ]

        return DoctorDashboardSummary(
            total_patients=total_patients,
            critical_risk_count=crit_count,
            high_risk_count=high_count,
            moderate_risk_count=mod_count,
            low_risk_count=low_count,
            pending_reviews_count=crit_count + high_count,
            recent_critical_patients=recent_items
        )

    @staticmethod
    async def get_patient_roster(
        db: AsyncSession,
        risk_category: Optional[RiskCategory] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[DoctorPatientListItem]:
        stmt = (
            select(PatientProfile)
            .join(PatientProfile.user)
            .options(
                selectinload(PatientProfile.user),
                selectinload(PatientProfile.assessments)
            )
        )
        if search:
            stmt = stmt.where(
                or_(
                    User.full_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%")
                )
            )

        res = await db.execute(stmt)
        patients = res.scalars().all()

        items = []
        for p in patients:
            latest_a = None
            if p.assessments:
                sorted_a = sorted(p.assessments, key=lambda x: x.assessed_at, reverse=True)
                latest_a = sorted_a[0]

            if risk_category and latest_a and latest_a.risk_category != risk_category:
                continue

            items.append(
                DoctorPatientListItem(
                    patient_id=p.id,
                    user_id=p.user_id,
                    full_name=p.user.full_name,
                    email=p.user.email,
                    age=latest_a.age if latest_a else None,
                    gender=p.gender.value if p.gender else "OTHER",
                    latest_risk_score=latest_a.overall_risk_score if latest_a else None,
                    latest_risk_category=latest_a.risk_category if latest_a else None,
                    latest_assessed_at=latest_a.assessed_at if latest_a else None,
                    has_pending_review=latest_a is not None and len(latest_a.reviews) == 0
                )
            )

        return items

    @staticmethod
    async def submit_review(
        db: AsyncSession, doctor_user: User, data: ClinicalReviewCreate
    ) -> ClinicalReviewResponse:
        doctor_profile = doctor_user.doctor_profile
        if not doctor_profile:
            doctor_profile = DoctorProfile(
                user_id=doctor_user.id,
                license_number="MD-DEFAULT",
                specialization="Cardiology & Internal Medicine",
                hospital_affiliation="PulsePredict Clinical Network",
                is_approved=True,
                verification_documents={}
            )
            db.add(doctor_profile)
            await db.flush()

        stmt = select(HealthAssessment).where(HealthAssessment.id == data.assessment_id)
        assessment = (await db.execute(stmt)).scalars().first()
        if not assessment:
            raise EntityNotFoundException("HealthAssessment", data.assessment_id)

        review = ClinicalReview(
            assessment_id=data.assessment_id,
            doctor_id=doctor_profile.id,
            clinical_notes=data.clinical_notes,
            recommendation=data.recommendation,
            requires_followup=data.requires_followup,
            follow_up_date=data.follow_up_date
        )
        db.add(review)
        await db.commit()
        await db.refresh(review)

        return ClinicalReviewResponse(
            id=review.id,
            assessment_id=review.assessment_id,
            doctor_id=review.doctor_id,
            doctor_name=doctor_user.full_name,
            specialization=doctor_profile.specialization,
            clinical_notes=review.clinical_notes,
            recommendation=review.recommendation,
            requires_followup=review.requires_followup,
            follow_up_date=review.follow_up_date,
            reviewed_at=review.reviewed_at
        )
