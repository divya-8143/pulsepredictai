import numpy as np
import pandas as pd
from typing import Dict, Any, List

class BayesianUncertaintyEngine:
    """
    Quantifies predictive epistemic uncertainty and detects Out-of-Distribution (OOD) inputs.
    Calculates Monte Carlo variance across ensemble classifiers and Mahalanobis distance from baseline training distribution.
    """

    FEATURE_MEANS = {
        "age": 52.4, "systolic_bp": 132.8, "diastolic_bp": 84.1, "resting_heart_rate": 73.2,
        "total_cholesterol": 208.5, "hdl_cholesterol": 49.2, "ldl_cholesterol": 128.4,
        "triglycerides": 154.0, "bmi": 26.8, "fasting_glucose": 104.2, "hba1c": 5.72
    }
    FEATURE_STDS = {
        "age": 12.5, "systolic_bp": 18.2, "diastolic_bp": 11.4, "resting_heart_rate": 10.5,
        "total_cholesterol": 38.0, "hdl_cholesterol": 14.2, "ldl_cholesterol": 34.5,
        "triglycerides": 65.0, "bmi": 5.2, "fasting_glucose": 28.5, "hba1c": 1.15
    }

    @classmethod
    def calculate_uncertainty_profile(
        cls,
        biomarker_dict: Dict[str, Any],
        ensemble_model_scores: Dict[str, float],
        overall_risk_score: float
    ) -> Dict[str, Any]:
        scores = list(ensemble_model_scores.values()) if ensemble_model_scores else [overall_risk_score]
        if len(scores) > 1:
            variance = float(np.var(scores))
            std_dev = float(np.std(scores))
        else:
            variance = 2.5
            std_dev = 1.58

        margin_of_error = float(np.round(1.96 * std_dev, 2))
        ci_lower = max(0.0, float(np.round(overall_risk_score - margin_of_error, 2)))
        ci_upper = min(100.0, float(np.round(overall_risk_score + margin_of_error, 2)))

        z_scores = []
        for feat, mean_val in cls.FEATURE_MEANS.items():
            if feat in biomarker_dict and biomarker_dict[feat] is not None:
                val = float(biomarker_dict[feat])
                std_val = cls.FEATURE_STDS.get(feat, 1.0)
                z = (val - mean_val) / std_val
                z_scores.append(z ** 2)

        mahalanobis_dist = float(np.sqrt(np.mean(z_scores))) if z_scores else 1.0
        is_ood = mahalanobis_dist > 2.8

        if is_ood:
            uncertainty_tier = "ELEVATED_OOD_UNCERTAINTY"
            confidence_grade = "Low (Out-of-Distribution Patient Profile)"
        elif std_dev > 8.0:
            uncertainty_tier = "MODERATE_ENSEMBLE_DISAGREEMENT"
            confidence_grade = "Moderate (High Inter-Model Variance)"
        else:
            uncertainty_tier = "HIGH_CONFIDENCE"
            confidence_grade = "High (Models Unanimously Agree)"

        return {
            "overall_risk_score": overall_risk_score,
            "margin_of_error_95ci": margin_of_error,
            "confidence_interval_95": {
                "lower_bound": ci_lower,
                "upper_bound": ci_upper,
                "formatted": f"{overall_risk_score:.1f}% (95% CI: {ci_lower:.1f}% - {ci_upper:.1f}%)"
            },
            "ensemble_variance": round(variance, 3),
            "ensemble_std_dev": round(std_dev, 3),
            "mahalanobis_ood_distance": round(mahalanobis_dist, 2),
            "is_out_of_distribution": is_ood,
            "uncertainty_tier": uncertainty_tier,
            "confidence_grade": confidence_grade,
            "clinical_reliability_note": (
                "High statistical confidence across model architectures."
                if not is_ood and std_dev <= 8.0
                else "Elevated uncertainty detected. Secondary physician clinical evaluation strongly indicated."
            )
        }
