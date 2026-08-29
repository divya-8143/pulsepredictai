"""
ISCHEMIA: Initial Invasive vs Conservative Strategy for Stable Coronary Disease
Citation: Maron et al. N Engl J Med 2020
Hazard Ratio / Effect: 0.93 (0.80-1.08) | Field: Cardiology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class IschemiaTrialEvidenceEngine:
    """
    Evidence-based clinical trial representation for ISCHEMIA: Initial Invasive vs Conservative Strategy for Stable Coronary Disease.
    """

    TRIAL_NAME = "ISCHEMIA: Initial Invasive vs Conservative Strategy for Stable Coronary Disease"
    CITATION = "Maron et al. N Engl J Med 2020"
    PRIMARY_EFFECT = "0.93 (0.80-1.08)"
    SPECIALTY = "Cardiology"

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
