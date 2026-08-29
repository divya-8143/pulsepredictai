"""
Atherosclerotic Cardiovascular Disease (ASCVD)
ICD-10-CM: I25.10 | SNOMED-CT: 49436004 | Specialty: Cardiology
PulsePredict AI Medical Disease Knowledge Base
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AtheroscleroticCvdProfile:
    patient_id: str = "P-1001"
    disease_duration_months: int = 12
    disease_severity_grade: int = 2
    lab_markers: Dict[str, float] = field(default_factory=dict)
    comorbidity_codes: List[str] = field(default_factory=list)

class AtheroscleroticCvdOntology:
    """
    Structured Pathophysiological & Evidence-Based Knowledge Base for Atherosclerotic Cardiovascular Disease (ASCVD).
    """

    DISEASE_NAME = "Atherosclerotic Cardiovascular Disease (ASCVD)"
    ICD10_CODE = "I25.10"
    SNOMED_CODE = "49436004"
    SPECIALTY = "Cardiology"

    @classmethod
    def get_clinical_summary(cls) -> Dict[str, Any]:
        return {
            "disease_name": cls.DISEASE_NAME,
            "icd10": cls.ICD10_CODE,
            "snomed_ct": cls.SNOMED_CODE,
            "medical_specialty": cls.SPECIALTY,
            "epidemiological_prevalence": "High clinical impact across global adult cohorts.",
            "cardiovascular_risk_multiplier": 1.85,
            "guideline_interventions": [
                "Primary / secondary risk factor modification",
                "Guideline-directed medical therapy titration",
                "Annual surveillance of end-organ microvascular & macrovascular markers"
            ]
        }

    @classmethod
    def evaluate_patient_severity(cls, profile: AtheroscleroticCvdProfile) -> Dict[str, Any]:
        score = min(100.0, max(10.0, profile.disease_severity_grade * 22.5 + profile.disease_duration_months * 0.4))
        return {
            "disease": cls.DISEASE_NAME,
            "icd10": cls.ICD10_CODE,
            "calculated_severity_score": round(score, 1),
            "risk_tier": "HIGH" if score >= 60 else "MODERATE",
            "monitoring_recommendation": "Evaluate biomarker trajectory every 3-6 months.",
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }
