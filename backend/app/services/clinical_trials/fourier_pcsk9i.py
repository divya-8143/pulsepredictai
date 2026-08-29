"""
FOURIER Trial: Evolocumab in Secondary Atherosclerotic Prevention
Citation: Sabatine et al. N Engl J Med 2017
Hazard Ratio / Effect: 0.85 (0.79-0.92) | Field: Lipidology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class FourierPcsk9IEvidenceEngine:
    """
    Evidence-based clinical trial representation for FOURIER Trial: Evolocumab in Secondary Atherosclerotic Prevention.
    """

    TRIAL_NAME = "FOURIER Trial: Evolocumab in Secondary Atherosclerotic Prevention"
    CITATION = "Sabatine et al. N Engl J Med 2017"
    PRIMARY_EFFECT = "0.85 (0.79-0.92)"
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
