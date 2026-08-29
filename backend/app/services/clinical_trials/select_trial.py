"""
SELECT: Semaglutide and Cardiovascular Outcomes in Obesity without Diabetes
Citation: Lincoff et al. N Engl J Med 2023
Hazard Ratio / Effect: 0.80 (0.72-0.90) | Field: Cardiovascular
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class SelectTrialEvidenceEngine:
    """
    Evidence-based clinical trial representation for SELECT: Semaglutide and Cardiovascular Outcomes in Obesity without Diabetes.
    """

    TRIAL_NAME = "SELECT: Semaglutide and Cardiovascular Outcomes in Obesity without Diabetes"
    CITATION = "Lincoff et al. N Engl J Med 2023"
    PRIMARY_EFFECT = "0.80 (0.72-0.90)"
    SPECIALTY = "Cardiovascular"

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
