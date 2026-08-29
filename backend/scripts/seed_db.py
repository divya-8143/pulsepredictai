import os
import sys
import asyncio
import uuid
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.patient import PatientProfile
from app.models.doctor import DoctorProfile
from app.models.assessment import HealthAssessment
from app.models.clinical_review import ClinicalReview
from app.models.enums import UserRole, Gender, SmokingStatus, AlcoholConsumption, RiskCategory, ReviewRecommendation
from app.schemas.assessment import HealthDataInput
from app.services.ml_inference_service import MLInferenceService

async def seed_database():
    print(f"Connecting to database {settings.DATABASE_URL}...")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with SessionLocal() as db:
        print("Checking existing seed users...")
        res = await db.execute(select(User).where(User.email == "admin@pulsepredict.ai"))
        if res.scalars().first():
            print("Database already seeded with root users. Skipping.")
            return

        # 1. Admin User
        admin_user = User(
            email="admin@pulsepredict.ai",
            hashed_password=get_password_hash("Password123!"),
            full_name="System Administrator",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        db.add(admin_user)

        # 2. Doctor User
        doctor_user = User(
            email="doctor.demo@pulsepredict.ai",
            hashed_password=get_password_hash("Password123!"),
            full_name="Dr. Sarah Jenkins, MD",
            role=UserRole.DOCTOR,
            is_active=True,
            is_verified=True
        )
        db.add(doctor_user)
        await db.flush()

        doc_profile = DoctorProfile(
            user_id=doctor_user.id,
            license_number="MD-2026-CARDIO-889",
            specialization="Cardiovascular Medicine & Interventional Cardiology",
            hospital_affiliation="PulsePredict University Hospital",
            is_approved=True,
            verification_documents={"verified_by": "State Medical Board"}
        )
        db.add(doc_profile)

        # 3. Patient User
        patient_user = User(
            email="patient.demo@pulsepredict.ai",
            hashed_password=get_password_hash("Password123!"),
            full_name="Emily Watson",
            role=UserRole.PATIENT,
            is_active=True,
            is_verified=True
        )
        db.add(patient_user)
        await db.flush()

        pat_profile = PatientProfile(
            user_id=patient_user.id,
            gender=Gender.FEMALE,
            blood_group="A+",
            phone_number="+1 (555) 234-5678",
            emergency_contact="David Watson (Spouse) - +1 (555) 876-5432",
            medical_history_flags={"allergies": ["Penicillin"], "surgeries": []}
        )
        db.add(pat_profile)
        await db.flush()

        # 4. Generate Historical Assessments for Emily
        print("Generating historical ML assessments for demo patient...")
        sample_inputs = [
            HealthDataInput(
                age=48.0, systolic_bp=142.0, diastolic_bp=92.0, resting_heart_rate=78.0,
                total_cholesterol=235.0, hdl_cholesterol=42.0, ldl_cholesterol=155.0, triglycerides=190.0,
                bmi=28.4, fasting_glucose=118.0, hba1c=6.1, smoking_status=SmokingStatus.CURRENT,
                alcohol_consumption=AlcoholConsumption.MODERATE, physical_activity_hours_week=1.5,
                family_history_cad=True, family_history_diabetes=True, family_history_hypertension=True
            ),
            HealthDataInput(
                age=48.0, systolic_bp=134.0, diastolic_bp=86.0, resting_heart_rate=74.0,
                total_cholesterol=215.0, hdl_cholesterol=46.0, ldl_cholesterol=138.0, triglycerides=165.0,
                bmi=27.2, fasting_glucose=104.0, hba1c=5.8, smoking_status=SmokingStatus.FORMER,
                alcohol_consumption=AlcoholConsumption.NONE, physical_activity_hours_week=3.0,
                family_history_cad=True, family_history_diabetes=True, family_history_hypertension=True
            ),
            HealthDataInput(
                age=49.0, systolic_bp=122.0, diastolic_bp=78.0, resting_heart_rate=70.0,
                total_cholesterol=192.0, hdl_cholesterol=52.0, ldl_cholesterol=112.0, triglycerides=140.0,
                bmi=25.6, fasting_glucose=94.0, hba1c=5.4, smoking_status=SmokingStatus.NEVER,
                alcohol_consumption=AlcoholConsumption.NONE, physical_activity_hours_week=4.5,
                family_history_cad=True, family_history_diabetes=True, family_history_hypertension=True
            )
        ]

        latest_assessment = None
        for idx, inp in enumerate(sample_inputs):
            inf = MLInferenceService.run_risk_assessment(inp)
            ass_time = datetime.utcnow() - timedelta(days=(len(sample_inputs) - idx) * 60)
            a = HealthAssessment(
                patient_id=pat_profile.id,
                age=inp.age,
                systolic_bp=inp.systolic_bp,
                diastolic_bp=inp.diastolic_bp,
                resting_heart_rate=inp.resting_heart_rate,
                total_cholesterol=inp.total_cholesterol,
                hdl_cholesterol=inp.hdl_cholesterol,
                ldl_cholesterol=inp.ldl_cholesterol,
                triglycerides=inp.triglycerides,
                bmi=inp.bmi,
                fasting_glucose=inp.fasting_glucose,
                hba1c=inp.hba1c,
                smoking_status=inp.smoking_status,
                alcohol_consumption=inp.alcohol_consumption,
                physical_activity_hours_week=inp.physical_activity_hours_week,
                family_history_cad=inp.family_history_cad,
                family_history_diabetes=inp.family_history_diabetes,
                family_history_hypertension=inp.family_history_hypertension,
                overall_risk_score=inf["overall_risk_score"],
                risk_category=inf["risk_category"],
                primary_model_name=inf["primary_model_name"],
                ensemble_predictions=inf["ensemble_predictions"],
                feature_importance_shap=inf["feature_importance_shap"],
                assessed_at=ass_time
            )
            db.add(a)
            latest_assessment = a

        await db.flush()

        # 5. Doctor Review on First High-Risk Assessment
        if latest_assessment:
            review = ClinicalReview(
                assessment_id=latest_assessment.id,
                doctor_id=doc_profile.id,
                clinical_notes="Patient shows marked improvement after smoking cessation and dietary modification. Blood pressure has normalized from stage 1 hypertension to optimal baseline.",
                recommendation=ReviewRecommendation.LIFESTYLE_MOD,
                requires_followup=True,
                follow_up_date=datetime.utcnow().date() + timedelta(days=90)
            )
            db.add(review)

        await db.commit()
        print("Database seeded successfully with enterprise demo accounts and assessments!")

if __name__ == "__main__":
    asyncio.run(seed_database())
