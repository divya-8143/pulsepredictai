import pytest
from app.services.dietary_engine import PersonalizedDietaryEngine
from app.services.diet_pdf_service import DietPlanPDFService

def test_diet_plan_generation_dash():
    biomarkers = {
        "age": 55, "gender": "MALE", "bmi": 28.4, "systolic_bp": 145, "diastolic_bp": 92,
        "fasting_glucose": 95, "hba1c": 5.4, "total_cholesterol": 190, "ldl_cholesterol": 115,
        "triglycerides": 140, "physical_activity_hours_week": 2.0
    }
    plan = PersonalizedDietaryEngine.generate_diet_plan(biomarkers, "MODERATE")
    assert "daily_target_calories" in plan
    assert plan["daily_target_calories"] > 1200
    assert "DASH" in plan["primary_dietary_framework"]
    assert "daily_meal_plan" in plan
    assert "breakfast" in plan["daily_meal_plan"]

def test_diet_pdf_generation():
    biomarkers = {
        "age": 52, "gender": "MALE", "bmi": 29.0, "systolic_bp": 138, "diastolic_bp": 88,
        "fasting_glucose": 110, "hba1c": 5.8, "total_cholesterol": 215, "ldl_cholesterol": 135,
        "triglycerides": 160, "physical_activity_hours_week": 1.5
    }
    plan = PersonalizedDietaryEngine.generate_diet_plan(biomarkers, "MODERATE")
    pdf_buffer = DietPlanPDFService.generate_diet_pdf(plan, patient_name="John Doe", assessment_id="test-123")
    assert pdf_buffer is not None
    assert pdf_buffer.getvalue().startswith(b"%PDF")
