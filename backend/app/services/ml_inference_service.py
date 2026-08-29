import pandas as pd
import numpy as np
from typing import Dict, Any, List

from app.schemas.assessment import HealthDataInput, SHAPFeatureContribution
from app.models.enums import RiskCategory
from ml_engine.training.registry import ModelRegistryService
from ml_engine.evaluation.explainability import ExplainabilityEngine

class MLInferenceService:
    @staticmethod
    def run_risk_assessment(biomarkers: HealthDataInput) -> Dict[str, Any]:
        """
        Execute full inference pipeline: Ensemble + Base models + SHAP explainability.
        """
        registry = ModelRegistryService.get_instance()
        ensemble = registry.get_ensemble()

        # Build single row DataFrame
        input_dict = {
            "age": biomarkers.age,
            "systolic_bp": biomarkers.systolic_bp,
            "diastolic_bp": biomarkers.diastolic_bp,
            "resting_heart_rate": biomarkers.resting_heart_rate,
            "total_cholesterol": biomarkers.total_cholesterol,
            "hdl_cholesterol": biomarkers.hdl_cholesterol,
            "ldl_cholesterol": biomarkers.ldl_cholesterol,
            "triglycerides": biomarkers.triglycerides,
            "bmi": biomarkers.bmi,
            "fasting_glucose": biomarkers.fasting_glucose,
            "hba1c": biomarkers.hba1c,
            "smoking_status": biomarkers.smoking_status.value,
            "alcohol_consumption": biomarkers.alcohol_consumption.value,
            "physical_activity_hours_week": biomarkers.physical_activity_hours_week,
            "family_history_cad": float(biomarkers.family_history_cad),
            "family_history_diabetes": float(biomarkers.family_history_diabetes),
            "family_history_hypertension": float(biomarkers.family_history_hypertension),
        }
        df_sample = pd.DataFrame([input_dict])

        # Run Ensemble Breakdown
        breakdown = ensemble.predict_detailed_breakdown(df_sample)
        overall_score = float(breakdown["overall_risk_score"])
        category_str = breakdown["overall_risk_category"]
        risk_category = RiskCategory(category_str)

        # Run SHAP Explainability on best tree model (XGBoost or RF)
        explainer_model = registry.get_model("XGBoost") or registry.get_model("RandomForest") or registry.get_model("LogisticRegression")
        shap_contributions = ExplainabilityEngine.explain_patient_risk(explainer_model, df_sample)

        # Generate Clinical Actionable Recommendations
        recommendations = MLInferenceService._generate_recommendations(biomarkers, risk_category, shap_contributions)

        return {
            "overall_risk_score": overall_score,
            "risk_category": risk_category,
            "primary_model_name": "Calibrated Ensemble (LR + RF + XGBoost)",
            "ensemble_predictions": breakdown["models"],
            "feature_importance_shap": shap_contributions,
            "clinical_recommendations": recommendations,
            "input_biomarkers": biomarkers
        }

    @staticmethod
    def _generate_recommendations(data: HealthDataInput, category: RiskCategory, shap_list: List[Dict[str, Any]]) -> List[str]:
        recs = []
        if category in [RiskCategory.HIGH, RiskCategory.CRITICAL]:
            recs.append("Schedule a comprehensive clinical consultation with a cardiologist / internist.")
        
        if data.systolic_bp >= 140 or data.diastolic_bp >= 90:
            recs.append("Daily blood pressure monitoring recommended. Limit dietary sodium intake (< 2,000 mg/day).")
        
        if data.fasting_glucose >= 100 or data.hba1c >= 5.7:
            recs.append("Metabolic glycemic screening advised; adopt a low-glycemic Mediterranean or DASH dietary pattern.")
        
        if data.smoking_status.value == "CURRENT":
            recs.append("Smoking cessation therapy strongly advised to reduce acute vascular inflammation.")
        
        if data.bmi >= 25.0:
            recs.append(f"Structured aerobic exercise target: at least 150 minutes/week with caloric balance optimization.")
        
        if data.ldl_cholesterol >= 130.0:
            recs.append("Evaluate lipid panel with primary care physician for potential statin or lifestyle lipid therapy.")

        if not recs:
            recs.append("Maintain routine physical exercise, balanced nutrition, and annual preventive health screening.")

        return recs
