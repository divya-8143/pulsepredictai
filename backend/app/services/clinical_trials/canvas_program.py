"""
CANVAS Program: Canagliflozin and Cardiovascular and Renal Events in Type 2 Diabetes
Citation: Neal et al. N Engl J Med 2017
Hazard Ratio / Effect: 0.86 (0.75-0.97) | Field: Cardiorenal
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class CanvasProgramEvidenceEngine:
    """
    Evidence-based clinical trial representation for CANVAS Program: Canagliflozin and Cardiovascular and Renal Events in Type 2 Diabetes.
    """

    TRIAL_NAME = "CANVAS Program: Canagliflozin and Cardiovascular and Renal Events in Type 2 Diabetes"
    CITATION = "Neal et al. N Engl J Med 2017"
    PRIMARY_EFFECT = "0.86 (0.75-0.97)"
    SPECIALTY = "Cardiorenal"

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
