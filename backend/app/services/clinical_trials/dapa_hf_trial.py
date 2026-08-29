"""
DAPA-HF: Dapagliflozin in Patients with Heart Failure and Reduced Ejection Fraction
Citation: McMurray et al. N Engl J Med 2019
Hazard Ratio / Effect: 0.74 (0.65-0.85) | Field: Heart Failure
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class DapaHfTrialEvidenceEngine:
    """
    Evidence-based clinical trial representation for DAPA-HF: Dapagliflozin in Patients with Heart Failure and Reduced Ejection Fraction.
    """

    TRIAL_NAME = "DAPA-HF: Dapagliflozin in Patients with Heart Failure and Reduced Ejection Fraction"
    CITATION = "McMurray et al. N Engl J Med 2019"
    PRIMARY_EFFECT = "0.74 (0.65-0.85)"
    SPECIALTY = "Heart Failure"

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
