import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc
from sqlalchemy.orm import selectinload

from app.models.assessment import HealthAssessment
from app.models.patient import PatientProfile
from app.models.user import User
from app.models.enums import UserRole, RiskCategory
from app.schemas.assessment import (
    HealthDataInput, RiskAssessmentResponse, 
    PaginatedAssessmentHistory, AssessmentHistoryItem,
    SHAPFeatureContribution
)
from app.services.validation_service import BiomarkerValidationService
from app.services.ml_inference_service import MLInferenceService
from app.core.exceptions import EntityNotFoundException, ForbiddenException, ValidationException

class AssessmentService:
    @staticmethod
    async def create_assessment(
        db: AsyncSession, current_user: User, data: HealthDataInput, target_patient_id: Optional[uuid.UUID] = None
    ) -> RiskAssessmentResponse:
        # 1. Enforce physiological consistency
        BiomarkerValidationService.validate_physiological_coherence(data)

        # 2. Resolve patient profile
        if current_user.role == UserRole.PATIENT:
            patient_profile = current_user.patient_profile
            if not patient_profile:
                patient_profile = PatientProfile(user_id=current_user.id, medical_history_flags={})
                db.add(patient_profile)
                await db.flush()
            patient_id = patient_profile.id
        elif current_user.role in [UserRole.DOCTOR, UserRole.ADMIN]:
            if not target_patient_id:
                raise ValidationException("Doctor must specify a target patient ID to perform assessment.")
            patient_id = target_patient_id
        else:
            raise ForbiddenException("Unauthorized to submit assessments.")

        # 3. Run ML Inference Engine
        inference_result = MLInferenceService.run_risk_assessment(data)

        # 4. Persist Assessment in PostgreSQL
        new_assessment = HealthAssessment(
            patient_id=patient_id,
            age=data.age,
            systolic_bp=data.systolic_bp,
            diastolic_bp=data.diastolic_bp,
            resting_heart_rate=data.resting_heart_rate,
            total_cholesterol=data.total_cholesterol,
            hdl_cholesterol=data.hdl_cholesterol,
            ldl_cholesterol=data.ldl_cholesterol,
            triglycerides=data.triglycerides,
            bmi=data.bmi,
            fasting_glucose=data.fasting_glucose,
            hba1c=data.hba1c,
            smoking_status=data.smoking_status,
            alcohol_consumption=data.alcohol_consumption,
            physical_activity_hours_week=data.physical_activity_hours_week,
            family_history_cad=data.family_history_cad,
            family_history_diabetes=data.family_history_diabetes,
            family_history_hypertension=data.family_history_hypertension,
            overall_risk_score=inference_result["overall_risk_score"],
            risk_category=inference_result["risk_category"],
            primary_model_name=inference_result["primary_model_name"],
            ensemble_predictions=inference_result["ensemble_predictions"],
            feature_importance_shap=inference_result["feature_importance_shap"],
            assessed_at=datetime.utcnow()
        )
        db.add(new_assessment)
        await db.commit()
        await db.refresh(new_assessment)

        return RiskAssessmentResponse(
            id=new_assessment.id,
            patient_id=patient_id,
            overall_risk_score=new_assessment.overall_risk_score,
            risk_category=new_assessment.risk_category,
            primary_model_name=new_assessment.primary_model_name,
            ensemble_predictions=new_assessment.ensemble_predictions,
            feature_importance_shap=[
                SHAPFeatureContribution(**item) for item in new_assessment.feature_importance_shap
            ],
            clinical_recommendations=inference_result["clinical_recommendations"],
            input_biomarkers=data,
            assessed_at=new_assessment.assessed_at
        )

    @staticmethod
    async def get_assessment_by_id(
        db: AsyncSession, current_user: User, assessment_id: uuid.UUID
    ) -> RiskAssessmentResponse:
        stmt = (
            select(HealthAssessment)
            .where(HealthAssessment.id == assessment_id)
            .options(selectinload(HealthAssessment.patient).selectinload(PatientProfile.user))
        )
        res = await db.execute(stmt)
        record = res.scalars().first()
        if not record:
            raise EntityNotFoundException("HealthAssessment", assessment_id)

        # Authorization check
        if current_user.role == UserRole.PATIENT and record.patient.user_id != current_user.id:
            raise ForbiddenException("Cannot access another patient's medical records.")

        input_data = HealthDataInput(
            age=record.age,
            systolic_bp=record.systolic_bp,
            diastolic_bp=record.diastolic_bp,
            resting_heart_rate=record.resting_heart_rate,
            total_cholesterol=record.total_cholesterol,
            hdl_cholesterol=record.hdl_cholesterol,
            ldl_cholesterol=record.ldl_cholesterol,
            triglycerides=record.triglycerides,
            bmi=record.bmi,
            fasting_glucose=record.fasting_glucose,
            hba1c=record.hba1c,
            smoking_status=record.smoking_status,
            alcohol_consumption=record.alcohol_consumption,
            physical_activity_hours_week=record.physical_activity_hours_week,
            family_history_cad=record.family_history_cad,
            family_history_diabetes=record.family_history_diabetes,
            family_history_hypertension=record.family_history_hypertension
        )

        recs = MLInferenceService._generate_recommendations(
            input_data, record.risk_category, record.feature_importance_shap
        )

        return RiskAssessmentResponse(
            id=record.id,
            patient_id=record.patient_id,
            overall_risk_score=record.overall_risk_score,
            risk_category=record.risk_category,
            primary_model_name=record.primary_model_name,
            ensemble_predictions=record.ensemble_predictions,
            feature_importance_shap=[
                SHAPFeatureContribution(**item) for item in record.feature_importance_shap
            ],
            clinical_recommendations=recs,
            input_biomarkers=input_data,
            assessed_at=record.assessed_at
        )

    @staticmethod
    async def get_patient_history(
        db: AsyncSession,
        patient_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        risk_category: Optional[RiskCategory] = None
    ) -> PaginatedAssessmentHistory:
        query = select(HealthAssessment).where(HealthAssessment.patient_id == patient_id)
        if risk_category:
            query = query.where(HealthAssessment.risk_category == risk_category)

        count_query = select(func.count()).select_from(query.subquery())
        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        query = query.order_by(desc(HealthAssessment.assessed_at)).offset((page - 1) * page_size).limit(page_size)
        res = await db.execute(query)
        records = res.scalars().all()

        items = [
            AssessmentHistoryItem(
                id=r.id,
                patient_id=r.patient_id,
                age=r.age,
                systolic_bp=r.systolic_bp,
                diastolic_bp=r.diastolic_bp,
                bmi=r.bmi,
                fasting_glucose=r.fasting_glucose,
                total_cholesterol=r.total_cholesterol,
                overall_risk_score=r.overall_risk_score,
                risk_category=r.risk_category,
                assessed_at=r.assessed_at
            ) for r in records
        ]

        total_pages = max(1, (total + page_size - 1) // page_size)
        return PaginatedAssessmentHistory(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    async def get_longitudinal_trends(db: AsyncSession, patient_id: uuid.UUID) -> List[Dict[str, Any]]:
        stmt = (
            select(HealthAssessment)
            .where(HealthAssessment.patient_id == patient_id)
            .order_by(HealthAssessment.assessed_at.asc())
        )
        res = await db.execute(stmt)
        records = res.scalars().all()

        return [
            {
                "date": r.assessed_at.strftime("%Y-%m-%d"),
                "risk_score": r.overall_risk_score,
                "systolic_bp": r.systolic_bp,
                "diastolic_bp": r.diastolic_bp,
                "bmi": r.bmi,
                "fasting_glucose": r.fasting_glucose,
                "total_cholesterol": r.total_cholesterol,
                "risk_category": r.risk_category.value
            }
            for r in records
        ]
