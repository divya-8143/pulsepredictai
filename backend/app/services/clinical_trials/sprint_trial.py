"""
SPRINT: Intensive vs. Standard Blood-Pressure Control in High-Risk Adults
Citation: SPRINT Research Group. N Engl J Med 2015
Hazard Ratio / Effect: 0.75 (0.64-0.89) | Field: Hypertension
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class SprintTrialEvidenceEngine:
    """
    Evidence-based clinical trial representation for SPRINT: Intensive vs. Standard Blood-Pressure Control in High-Risk Adults.
    """

    TRIAL_NAME = "SPRINT: Intensive vs. Standard Blood-Pressure Control in High-Risk Adults"
    CITATION = "SPRINT Research Group. N Engl J Med 2015"
    PRIMARY_EFFECT = "0.75 (0.64-0.89)"
    SPECIALTY = "Hypertension"

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
