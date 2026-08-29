"""
CLEAR Outcomes: Bempedoic Acid and Cardiovascular Outcomes in Statin-Intolerant Patients
Citation: Nissen et al. N Engl J Med 2023
Hazard Ratio / Effect: 0.87 (0.79-0.96) | Field: Lipidology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class ClearOutcomesEvidenceEngine:
    """
    Evidence-based clinical trial representation for CLEAR Outcomes: Bempedoic Acid and Cardiovascular Outcomes in Statin-Intolerant Patients.
    """

    TRIAL_NAME = "CLEAR Outcomes: Bempedoic Acid and Cardiovascular Outcomes in Statin-Intolerant Patients"
    CITATION = "Nissen et al. N Engl J Med 2023"
    PRIMARY_EFFECT = "0.87 (0.79-0.96)"
    SPECIALTY = "Lipidology"

    @classmethod
    def get_trial_metadata(cls) -> Dict[str, Any]:
        return {
            "trial_name": cls.TRIAL_NAME,
            "citation": cls.CITATION,
            "primary_endpoint_effect": cls.PRIMARY_EFFECT,
            "specialty": cls.SPECIALTY,
            "clinical_takeaway": "Key landmark evidence supporting current class-I guideline recommendations.",
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
