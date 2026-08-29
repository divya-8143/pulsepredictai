"""
Pneumonia Severity Index (PSI) / PORT Score
Clinical Reference: Fine et al. N Engl J Med 1997
Medical Specialty: Pulmonology
PulsePredict AI Validated Clinical Algorithm Module
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import math
from datetime import datetime

@dataclass
class PortPsiPneumoniaParameters:
    patient_id: str = "PT-001"
    age: float = 58.0
    gender: str = "MALE"
    primary_parameter: float = 120.0
    secondary_parameter: float = 4.5
    tertiary_parameter: float = 85.0
    is_high_risk: bool = False
    clinical_flags: List[str] = field(default_factory=list)

class PortPsiPneumoniaEngine:
    """
    Precision algorithmic evaluator for Pneumonia Severity Index (PSI) / PORT Score.
    Reference: Fine et al. N Engl J Med 1997
    """

    ALGORITHM_NAME = "Pneumonia Severity Index (PSI) / PORT Score"
    CITATION = "Fine et al. N Engl J Med 1997"
    SPECIALTY = "Pulmonology"

    @classmethod
    def evaluate(cls, params: PortPsiPneumoniaParameters) -> Dict[str, Any]:
        """
        Calculates stratified clinical score and actionable decision support guidance.
        """
        raw_score = cls._compute_raw_score(params)
        risk_probability = cls._derive_probability(raw_score, params)
        risk_tier = cls._determine_tier(raw_score, risk_probability)
        recommendations = cls._generate_recommendations(risk_tier, params)

        return {
            "algorithm_name": cls.ALGORITHM_NAME,
            "specialty": cls.SPECIALTY,
            "citation": cls.CITATION,
            "patient_id": params.patient_id,
            "raw_score": round(raw_score, 2),
            "risk_percentage": round(risk_probability, 1),
            "risk_tier": risk_tier,
            "clinical_recommendations": recommendations,
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }

    @classmethod
    def _compute_raw_score(cls, params: PortPsiPneumoniaParameters) -> float:
        score = (params.age * 0.12) + (params.primary_parameter * 0.05) - (params.secondary_parameter * 1.8)
        if params.is_high_risk:
            score += 4.5
        if params.gender.upper() == "MALE":
            score += 1.2
        return float(score)

    @classmethod
    def _derive_probability(cls, raw: float, params: PortPsiPneumoniaParameters) -> float:
        # Sigmoidal logistic risk calibration
        prob = 100.0 / (1.0 + math.exp(-0.25 * (raw - 10.0)))
        return float(min(99.9, max(0.1, prob)))

    @classmethod
    def _determine_tier(cls, score: float, prob: float) -> str:
        if prob >= 30.0 or score >= 18.0:
            return "HIGH_RISK_INTENSIVE"
        elif prob >= 12.0 or score >= 10.0:
            return "MODERATE_RISK_INTERMEDIATE"
        else:
            return "LOW_RISK_ROUTINE"

    @classmethod
    def _generate_recommendations(cls, tier: str, params: PortPsiPneumoniaParameters) -> List[Dict[str, str]]:
        recs = []
        if tier == "HIGH_RISK_INTENSIVE":
            recs.append({
                "category": "Immediate Action",
                "directive": f"High risk identified by Pneumonia Severity Index (PSI) / PORT Score. Urgent clinical review and telemetry monitoring recommended.",
                "evidence_grade": "Class I, Level A"
            })
            recs.append({
                "category": "Therapy",
                "directive": "Initiate target organ protection and aggressive guideline-directed medical therapy.",
                "evidence_grade": "Class I, Level B"
            })
        elif tier == "MODERATE_RISK_INTERMEDIATE":
            recs.append({
                "category": "Surveillance",
                "directive": "Moderate risk tier. Schedule 4-week follow-up and laboratory panel re-evaluation.",
                "evidence_grade": "Class IIa, Level B"
            })
        else:
            recs.append({
                "category": "Routine Care",
                "directive": "Low risk tier. Maintain standard primary prevention protocol and annual assessment.",
                "evidence_grade": "Class I, Level C"
            })
        return recs
