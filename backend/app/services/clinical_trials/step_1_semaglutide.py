"""
STEP 1: Once-Weekly Semaglutide in Adults with Overweight or Obesity
Citation: Wilding et al. N Engl J Med 2021
Hazard Ratio / Effect: Weight -14.9% | Field: Metabolism
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class Step1SemaglutideEvidenceEngine:
    """
    Evidence-based clinical trial representation for STEP 1: Once-Weekly Semaglutide in Adults with Overweight or Obesity.
    """

    TRIAL_NAME = "STEP 1: Once-Weekly Semaglutide in Adults with Overweight or Obesity"
    CITATION = "Wilding et al. N Engl J Med 2021"
    PRIMARY_EFFECT = "Weight -14.9%"
    SPECIALTY = "Metabolism"

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
