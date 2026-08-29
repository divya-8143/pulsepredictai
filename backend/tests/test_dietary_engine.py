import pytest
from app.services.dietary_engine import PersonalizedDietaryEngine

def test_diet_plan_generation_dash():
    biomarkers = {
        "age": 55,
        "gender": "MALE",
        "bmi": 28.4,
        "systolic_bp": 145,
        "diastolic_bp": 92,
        "fasting_glucose": 95,
        "hba1c": 5.4,
        "total_cholesterol": 190,
        "ldl_cholesterol": 115,
        "triglycerides": 140,
        "physical_activity_hours_week": 2.0
    }
    plan = PersonalizedDietaryEngine.generate_diet_plan(biomarkers, "MODERATE")
    assert "daily_target_calories" in plan
    assert plan["daily_target_calories"] > 1200
    assert "DASH" in plan["primary_dietary_framework"]
    assert "daily_meal_plan" in plan
    assert "breakfast" in plan["daily_meal_plan"]

def test_diet_plan_generation_glycemic():
    biomarkers = {
        "age": 48,
        "gender": "FEMALE",
        "bmi": 31.0,
        "systolic_bp": 120,
        "diastolic_bp": 78,
        "fasting_glucose": 135,
        "hba1c": 6.8,
        "total_cholesterol": 210,
        "ldl_cholesterol": 130,
        "triglycerides": 180,
        "physical_activity_hours_week": 1.0
    }
    plan = PersonalizedDietaryEngine.generate_diet_plan(biomarkers, "HIGH")
    assert "Low-Glycemic" in plan["primary_dietary_framework"]
    assert len(plan["foods_to_embrace"]) > 0
    assert len(plan["foods_to_restrict"]) > 0
