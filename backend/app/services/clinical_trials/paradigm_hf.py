"""
PARADIGM-HF: Sacubitril/Valsartan (ARNI) versus Enalapril in Heart Failure
Citation: McMurray et al. N Engl J Med 2014
Hazard Ratio / Effect: 0.80 (0.73-0.87) | Field: Heart Failure
PulsePredict AI Clinical Trial Evidence Base
"""

from typing import Dict, Any, List
from datetime import datetime

class ParadigmHfEvidenceEngine:
    """
    Evidence-based clinical trial representation for PARADIGM-HF: Sacubitril/Valsartan (ARNI) versus Enalapril in Heart Failure.
    """

    TRIAL_NAME = "PARADIGM-HF: Sacubitril/Valsartan (ARNI) versus Enalapril in Heart Failure"
    CITATION = "McMurray et al. N Engl J Med 2014"
    PRIMARY_EFFECT = "0.80 (0.73-0.87)"
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
