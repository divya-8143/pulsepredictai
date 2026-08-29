"""
COLCOT: Efficacy and Safety of Low-Dose Colchicine after Myocardial Infarction
Citation: Tardif et al. N Engl J Med 2019
Hazard Ratio / Effect: 0.77 (0.61-0.96) | Field: Immunology
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class ColcotTrialEvidenceEngine:
    """
    Evidence-based clinical trial representation for COLCOT: Efficacy and Safety of Low-Dose Colchicine after Myocardial Infarction.
    """

    TRIAL_NAME = "COLCOT: Efficacy and Safety of Low-Dose Colchicine after Myocardial Infarction"
    CITATION = "Tardif et al. N Engl J Med 2019"
    PRIMARY_EFFECT = "0.77 (0.61-0.96)"
    SPECIALTY = "Immunology"

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
