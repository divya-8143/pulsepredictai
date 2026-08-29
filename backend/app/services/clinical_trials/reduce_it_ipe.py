"""
REDUCE-IT: Cardiovascular Risk Reduction with Icosapent Ethyl for Hypertriglyceridemia
Citation: Bhatt et al. N Engl J Med 2019
Hazard Ratio / Effect: 0.75 (0.68-0.83) | Field: Lipidology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class ReduceItIpeEvidenceEngine:
    """
    Evidence-based clinical trial representation for REDUCE-IT: Cardiovascular Risk Reduction with Icosapent Ethyl for Hypertriglyceridemia.
    """

    TRIAL_NAME = "REDUCE-IT: Cardiovascular Risk Reduction with Icosapent Ethyl for Hypertriglyceridemia"
    CITATION = "Bhatt et al. N Engl J Med 2019"
    PRIMARY_EFFECT = "0.75 (0.68-0.83)"
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
