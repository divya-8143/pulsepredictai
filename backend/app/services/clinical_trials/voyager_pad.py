"""
VOYAGER PAD: Rivaroxaban in Peripheral Artery Disease after Revascularization
Citation: Bonaca et al. N Engl J Med 2020
Hazard Ratio / Effect: 0.85 (0.76-0.96) | Field: Vascular
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class VoyagerPadEvidenceEngine:
    """
    Evidence-based clinical trial representation for VOYAGER PAD: Rivaroxaban in Peripheral Artery Disease after Revascularization.
    """

    TRIAL_NAME = "VOYAGER PAD: Rivaroxaban in Peripheral Artery Disease after Revascularization"
    CITATION = "Bonaca et al. N Engl J Med 2020"
    PRIMARY_EFFECT = "0.85 (0.76-0.96)"
    SPECIALTY = "Vascular"

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
