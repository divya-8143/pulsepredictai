import numpy as np
import pandas as pd
from typing import Dict, Any, List
from app.schemas.assessment import HealthDataInput
from ml_engine.training.registry import ModelRegistryService
from ml_engine.evaluation.explainability import ExplainabilityEngine
from ml_engine.evaluation.uncertainty_engine import BayesianUncertaintyEngine
from app.services.anomaly_detection_service import BiomarkerAnomalyDetectionService
from app.core.cache import MultiTierInferenceCache
from app.core.logging import logger

class MLInferenceService:
    """
    High-throughput ML Inference Service with Multi-Tier Caching,
    Bayesian Uncertainty Estimation, and Biochemical Plausibility Checks.
    """

    @classmethod
    def run_risk_assessment(cls, biomarkers: HealthDataInput) -> Dict[str, Any]:
        raw_dict = biomarkers.model_dump()
        cache = MultiTierInferenceCache()
        cache_key = f"infer:{cache.generate_biomarker_hash(raw_dict)}"

        # Check Cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("Inference cache HIT (sub-5ms response).")
            cached_result["from_cache"] = True
            return cached_result

        # 1. Physiological Coherence Check
        coherence_report = BiomarkerAnomalyDetectionService.analyze_physiological_coherence(biomarkers)

        # 2. Prepare DataFrame
        df_sample = pd.DataFrame([raw_dict])
        df_sample = df_sample.rename(columns={
            "smoking_status": "smoking_status",
            "alcohol_consumption": "alcohol_consumption"
        })
        if hasattr(biomarkers.smoking_status, "value"):
            df_sample["smoking_status"] = biomarkers.smoking_status.value
        if hasattr(biomarkers.alcohol_consumption, "value"):
            df_sample["alcohol_consumption"] = biomarkers.alcohol_consumption.value

        df_sample["family_history_cad"] = float(df_sample["family_history_cad"].iloc[0])
        df_sample["family_history_diabetes"] = float(df_sample["family_history_diabetes"].iloc[0])
        df_sample["family_history_hypertension"] = float(df_sample["family_history_hypertension"].iloc[0])

        # 3. Model Registry & Multi-Model Inference
        registry = ModelRegistryService.get_instance()
        ensemble_model = registry.get_ensemble()

        breakdown = ensemble_model.predict_detailed_breakdown(df_sample)

        # 4. SHAP Feature Attribution
        explainer_model = ensemble_model.models.get("XGBoost") or list(ensemble_model.models.values())[0]
        shap_contributions = ExplainabilityEngine.explain_patient_risk(explainer_model, df_sample)

        # 5. Bayesian Uncertainty Quantification
        ensemble_scores = {
            m_name: float(m_info.get("predicted_risk_score", breakdown["overall_risk_score"]))
            for m_name, m_info in breakdown.get("models", {}).items()
        }
        uncertainty_profile = BayesianUncertaintyEngine.calculate_uncertainty_profile(
            biomarker_dict=raw_dict,
            ensemble_model_scores=ensemble_scores,
            overall_risk_score=breakdown["overall_risk_score"]
        )

        # 6. Actionable Clinical Recommendations
        recommendations = cls._generate_clinical_recommendations(breakdown["overall_risk_category"], biomarkers)

        result_payload = {
            "overall_risk_score": breakdown["overall_risk_score"],
            "risk_category": breakdown["overall_risk_category"],
            "primary_model_name": "Calibrated Multi-Model Ensemble (LR + RF + XGBoost)",
            "ensemble_predictions": breakdown.get("models", {}),
            "feature_importance_shap": shap_contributions,
            "clinical_recommendations": recommendations,
            "uncertainty_profile": uncertainty_profile,
            "physiological_coherence": coherence_report,
            "from_cache": False
        }

        # Store in cache
        cache.set(cache_key, result_payload, ttl_seconds=3600)
        return result_payload

    @staticmethod
    def _generate_clinical_recommendations(category: Any, data: HealthDataInput) -> List[str]:
        recs = []
        cat_str = str(category.value) if hasattr(category, "value") else str(category)

        if cat_str in ["HIGH", "CRITICAL"]:
            recs.append("Urgent comprehensive cardiovascular consultation and 12-lead ECG.")
            recs.append("Evaluate initiation of moderate-to-high intensity statin therapy.")
            recs.append("Strict home blood pressure surveillance targeting < 130/80 mmHg.")
        elif cat_str == "MODERATE":
            recs.append("Implement therapeutic lifestyle changes: Mediterranean diet & 150 min/wk aerobic exercise.")
            recs.append("Repeat fasting lipid panel and glycemic screening in 3-6 months.")
            recs.append("Consider Coronary Artery Calcium (CAC) scan for risk reclassification.")
        else:
            recs.append("Maintain optimal cardiovascular health baseline habits.")
            recs.append("Routine preventive biomarker re-evaluation in 12 months.")

        if data.smoking_status in ["CURRENT", "FORMER"]:
            recs.append("Active tobacco cessation counseling and nicotine replacement support.")
        if data.fasting_glucose >= 126 or data.hba1c >= 6.5:
            recs.append("Endocrine referral for individualized glycemic management.")
        return recs
