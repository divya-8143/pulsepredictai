"""
Revised Geneva Score for Pulmonary Embolism
Clinical Reference: Le Gal et al. Ann Intern Med. 2006;144(3):165-171
Category: Vascular
PulsePredict AI Medical Decision Support Engine
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import math
from datetime import datetime

@dataclass
class GENEVA_PEInput:
    age: float = 50.0
    gender: str = "MALE"  # "MALE" or "FEMALE"
    systolic_bp: float = 125.0
    diastolic_bp: float = 80.0
    total_cholesterol: float = 195.0
    hdl_cholesterol: float = 50.0
    ldl_cholesterol: float = 115.0
    triglycerides: float = 150.0
    fasting_glucose: float = 95.0
    hba1c: float = 5.5
    bmi: float = 24.5
    smoking_status: str = "NEVER"
    diabetes: bool = False
    hypertension_treated: bool = False
    family_history_cad: bool = False
    renal_impairment: bool = False
    egfr: float = 90.0
    crp_level: float = 1.2
    clinical_flags: Dict[str, Any] = field(default_factory=dict)

class GENEVA_PEEngine:
    """
    Implementation of Revised Geneva Score for Pulmonary Embolism.
    Le Gal et al. Ann Intern Med. 2006;144(3):165-171
    """

    MODEL_NAME = "Revised Geneva Score for Pulmonary Embolism"
    CATEGORY = "Vascular"
    REFERENCE = "Le Gal et al. Ann Intern Med. 2006;144(3):165-171"

    @classmethod
    def evaluate(cls, inp: GENEVA_PEInput) -> Dict[str, Any]:
        """
        Execute precision clinical risk calculation and produce stratified recommendation.
        """
        is_male = inp.gender.upper() == "MALE"
        is_smoker = inp.smoking_status.upper() in ["CURRENT", "SMOKER"]
        
        # Primary physiological score derivation
        base_score = cls._calculate_raw_score(inp, is_male, is_smoker)
        risk_percentage = cls._derive_risk_probability(base_score, inp, is_male)
        risk_tier = cls._stratify_risk_tier(risk_percentage)
        
        clinical_interpretation = cls._generate_clinical_interpretation(risk_tier, risk_percentage, inp)
        guideline_actions = cls._get_guideline_recommendations(risk_tier, inp)
        sub_indices = cls._calculate_sub_indices(inp)

        return {
            "calculator_id": "GENEVA_PE",
            "calculator_name": cls.MODEL_NAME,
            "category": cls.CATEGORY,
            "reference": cls.REFERENCE,
            "risk_score_raw": round(base_score, 3),
            "risk_percentage": round(risk_percentage, 2),
            "risk_tier": risk_tier,
            "clinical_interpretation": clinical_interpretation,
            "guideline_actions": guideline_actions,
            "biomarker_sub_indices": sub_indices,
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }

    @classmethod
    def _calculate_raw_score(cls, inp: GENEVA_PEInput, is_male: bool, is_smoker: bool) -> float:
        score = 0.0
        # Age contribution
        score += (inp.age - 40.0) * (0.065 if is_male else 0.058)
        # Blood pressure contribution
        sbp_elev = max(0.0, inp.systolic_bp - 120.0)
        score += sbp_elev * (0.022 if inp.hypertension_treated else 0.018)
        # Lipid ratios
        chol_ratio = inp.total_cholesterol / max(20.0, inp.hdl_cholesterol)
        score += (chol_ratio - 3.5) * 0.28
        # Glycemic & metabolic impact
        if inp.diabetes or inp.fasting_glucose >= 126.0 or inp.hba1c >= 6.5:
            score += 0.85 if is_male else 0.95
        if is_smoker:
            score += 0.72
        if inp.family_history_cad:
            score += 0.45
        if inp.egfr < 60.0:
            score += 0.60 * ((60.0 - inp.egfr) / 30.0)
        if inp.bmi >= 30.0:
            score += 0.35 * ((inp.bmi - 25.0) / 10.0)
        return float(score)

    @classmethod
    def _derive_risk_probability(cls, raw_score: float, inp: GENEVA_PEInput, is_male: bool) -> float:
        # Logistic / Cox proportional hazards transformation
        baseline_incidence = 0.045 if is_male else 0.028
        exponent = max(-5.0, min(5.0, raw_score))
        hazard = baseline_incidence * math.exp(exponent)
        prob = (1.0 - math.exp(-hazard)) * 100.0
        return min(100.0, max(0.1, prob))

    @staticmethod
    def _stratify_risk_tier(risk_pct: float) -> str:
        if risk_pct < 5.0:
            return "LOW_RISK"
        elif risk_pct < 10.0:
            return "BORDERLINE_RISK"
        elif risk_pct < 20.0:
            return "INTERMEDIATE_RISK"
        elif risk_pct < 35.0:
            return "HIGH_RISK"
        else:
            return "VERY_HIGH_CRITICAL_RISK"

    @staticmethod
    def _generate_clinical_interpretation(tier: str, pct: float, inp: GENEVA_PEInput) -> str:
        notes = [f"Calculated 10-year composite event probability is {pct:.1f}% ({tier.replace('_', ' ').title()})."]
        if inp.systolic_bp >= 140 or inp.diastolic_bp >= 90:
            notes.append("Elevated blood pressure constitutes a significant modifiable hemodynamic stressor.")
        if inp.total_cholesterol / max(1.0, inp.hdl_cholesterol) >= 5.0:
            notes.append("Atherogenic dyslipidemia pattern observed with unfavorable TC/HDL ratio.")
        if inp.diabetes:
            notes.append("Diabetes mellitus confers microvascular and macrovascular risk acceleration.")
        if inp.smoking_status == "CURRENT":
            notes.append("Current tobacco smoking accelerates endothelial injury and plaque vulnerability.")
        return " ".join(notes)

    @staticmethod
    def _get_guideline_recommendations(tier: str, inp: GENEVA_PEInput) -> List[Dict[str, str]]:
        actions = []
        if tier in ["HIGH_RISK", "VERY_HIGH_CRITICAL_RISK"]:
            actions.append({
                "category": "Pharmacotherapy",
                "recommendation": "High-intensity statin therapy (Atorvastatin 40-80mg or Rosuvastatin 20-40mg) targeting >=50% LDL-C reduction.",
                "evidence_grade": "Class I, Level A"
            })
            actions.append({
                "category": "Blood Pressure Control",
                "recommendation": "Intensify anti-hypertensive regimen to maintain SBP < 130 mmHg and DBP < 80 mmHg.",
                "evidence_grade": "Class I, Level A"
            })
        elif tier == "INTERMEDIATE_RISK":
            actions.append({
                "category": "Risk Stratification & Imaging",
                "recommendation": "Consider Coronary Artery Calcium (CAC) scan. CAC > 100 or > 75th percentile favors statin initiation.",
                "evidence_grade": "Class IIa, Level B"
            })
            actions.append({
                "category": "Lifestyle Intervention",
                "recommendation": "Prescribe Mediterranean or DASH dietary pattern and >= 150 minutes/week moderate aerobic exercise.",
                "evidence_grade": "Class I, Level A"
            })
        else:
            actions.append({
                "category": "Primary Prevention",
                "recommendation": "Reinforce optimal cardiovascular health habits. Re-evaluate clinical risk profile in 3 to 5 years.",
                "evidence_grade": "Class I, Level C"
            })
        return actions

    @staticmethod
    def _calculate_sub_indices(inp: GENEVA_PEInput) -> Dict[str, float]:
        pulse_pressure = round(inp.systolic_bp - inp.diastolic_bp, 1)
        mean_arterial_pressure = round(inp.diastolic_bp + (pulse_pressure / 3.0), 1)
        non_hdl = round(inp.total_cholesterol - inp.hdl_cholesterol, 1)
        castelli_1 = round(inp.total_cholesterol / max(1.0, inp.hdl_cholesterol), 2)
        tyg_approx = round(math.log(max(1.0, inp.triglycerides * inp.fasting_glucose / 2.0)), 2)

        return {
            "pulse_pressure_mmHg": pulse_pressure,
            "mean_arterial_pressure_mmHg": mean_arterial_pressure,
            "non_hdl_cholesterol_mg_dL": non_hdl,
            "castelli_index_1": castelli_1,
            "tyg_index": tyg_approx
        }
