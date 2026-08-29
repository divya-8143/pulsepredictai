"""Metabolic Syndrome (MetS) Harmonized Criteria Scorer"""
from typing import Dict, Any

class MetabolicSyndromeScorer:
    @classmethod
    def evaluate_mets(
        cls, waist_cm: float, sbp: float, dbp: float,
        fasting_glucose: float, tg: float, hdl: float, is_male: bool
    ) -> Dict[str, Any]:
        criteria_met = 0
        reasons = []
        if (is_male and waist_cm >= 102) or (not is_male and waist_cm >= 88):
            criteria_met += 1
            reasons.append("Abdominal Obesity")
        if sbp >= 130 or dbp >= 85:
            criteria_met += 1
            reasons.append("Elevated Blood Pressure")
        if fasting_glucose >= 100:
            criteria_met += 1
            reasons.append("Impaired Fasting Glucose")
        if tg >= 150:
            criteria_met += 1
            reasons.append("Hypertriglyceridemia")
        if (is_male and hdl < 40) or (not is_male and hdl < 50):
            criteria_met += 1
            reasons.append("Low HDL-C")

        return {
            "criteria_count": criteria_met,
            "metabolic_syndrome_diagnosed": criteria_met >= 3,
            "positive_components": reasons
        }
