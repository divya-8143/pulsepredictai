"""
ODYSSEY OUTCOMES: Alirocumab in Post-ACS Cardiovascular Protection
Citation: Schwartz et al. N Engl J Med 2018
Hazard Ratio / Effect: 0.85 (0.78-0.93) | Field: Lipidology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class OdysseyOutcomesEvidenceEngine:
    """
    Evidence-based clinical trial representation for ODYSSEY OUTCOMES: Alirocumab in Post-ACS Cardiovascular Protection.
    """

    TRIAL_NAME = "ODYSSEY OUTCOMES: Alirocumab in Post-ACS Cardiovascular Protection"
    CITATION = "Schwartz et al. N Engl J Med 2018"
    PRIMARY_EFFECT = "0.85 (0.78-0.93)"
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
