"""
Type 2 Diabetes Mellitus with Vascular Complications
ICD-10-CM: E11.9 | SNOMED-CT: 44054006 | Specialty: Endocrinology
PulsePredict AI Medical Disease Knowledge Base
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Type2DiabetesMellitusProfile:
    patient_id: str = "P-1001"
    disease_duration_months: int = 12
    disease_severity_grade: int = 2
    lab_markers: Dict[str, float] = field(default_factory=dict)
    comorbidity_codes: List[str] = field(default_factory=list)

class Type2DiabetesMellitusOntology:
    """
    Structured Pathophysiological & Evidence-Based Knowledge Base for Type 2 Diabetes Mellitus with Vascular Complications.
    """

    DISEASE_NAME = "Type 2 Diabetes Mellitus with Vascular Complications"
    ICD10_CODE = "E11.9"
    SNOMED_CODE = "44054006"
    SPECIALTY = "Endocrinology"

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
    def evaluate_patient_severity(cls, profile: Type2DiabetesMellitusProfile) -> Dict[str, Any]:
        score = min(100.0, max(10.0, profile.disease_severity_grade * 22.5 + profile.disease_duration_months * 0.4))
        return {
            "disease": cls.DISEASE_NAME,
            "icd10": cls.ICD10_CODE,
            "calculated_severity_score": round(score, 1),
            "risk_tier": "HIGH" if score >= 60 else "MODERATE",
            "monitoring_recommendation": "Evaluate biomarker trajectory every 3-6 months.",
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }
