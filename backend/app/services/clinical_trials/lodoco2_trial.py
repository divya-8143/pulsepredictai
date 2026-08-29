"""
LoDoCo2: Colchicine in Patients with Chronic Coronary Disease
Citation: Nidorf et al. N Engl J Med 2020
Hazard Ratio / Effect: 0.72 (0.57-0.92) | Field: Cardiology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class Lodoco2TrialEvidenceEngine:
    """
    Evidence-based clinical trial representation for LoDoCo2: Colchicine in Patients with Chronic Coronary Disease.
    """

    TRIAL_NAME = "LoDoCo2: Colchicine in Patients with Chronic Coronary Disease"
    CITATION = "Nidorf et al. N Engl J Med 2020"
    PRIMARY_EFFECT = "0.72 (0.57-0.92)"
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
