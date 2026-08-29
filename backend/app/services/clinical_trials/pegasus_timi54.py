"""
PEGASUS-TIMI 54: Long-Term Ticagrelor in Patients with Prior Myocardial Infarction
Citation: Bonaca et al. N Engl J Med 2015
Hazard Ratio / Effect: 0.84 (0.74-0.95) | Field: Cardiology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class PegasusTimi54EvidenceEngine:
    """
    Evidence-based clinical trial representation for PEGASUS-TIMI 54: Long-Term Ticagrelor in Patients with Prior Myocardial Infarction.
    """

    TRIAL_NAME = "PEGASUS-TIMI 54: Long-Term Ticagrelor in Patients with Prior Myocardial Infarction"
    CITATION = "Bonaca et al. N Engl J Med 2015"
    PRIMARY_EFFECT = "0.84 (0.74-0.95)"
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
