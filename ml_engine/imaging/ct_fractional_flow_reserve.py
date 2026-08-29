"""
CT-Derived Fractional Flow Reserve (FFR-CT) Hemodynamic Lesion
Category: Radiology
PulsePredict AI Cardiovascular Imaging Engine
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import math
from datetime import datetime

@dataclass
class CtFractionalFlowReserveParameters:
    measured_dimension_mm: float = 45.0
    flow_velocity_ms: float = 1.2
    bsa_m2: float = 1.95
    is_stress_test: bool = False
    patient_notes: str = ""

class CtFractionalFlowReserveCalculator:
    """
    Precision quantification and guideline grading for CT-Derived Fractional Flow Reserve (FFR-CT) Hemodynamic Lesion.
    """

    EXAM_NAME = "CT-Derived Fractional Flow Reserve (FFR-CT) Hemodynamic Lesion"
    MODALITY = "Radiology"

    @classmethod
    def calculate_imaging_index(cls, params: CtFractionalFlowReserveParameters) -> Dict[str, Any]:
        """
        Calculates standardized indexed parameters based on ASE/EACVI guidelines.
        """
        indexed_value = params.measured_dimension_mm / max(1.0, params.bsa_m2)
        severity = "NORMAL"
        if indexed_value >= 40.0:
            severity = "SEVERE_ENLARGEMENT"
        elif indexed_value >= 32.0:
            severity = "MODERATE_ALTERATION"
        elif indexed_value >= 28.0:
            severity = "MILD_ALTERATION"

        return {
            "exam_name": cls.EXAM_NAME,
            "modality": cls.MODALITY,
            "raw_measurement": params.measured_dimension_mm,
            "body_surface_area_m2": params.bsa_m2,
            "indexed_value": round(indexed_value, 2),
            "grading_tier": severity,
            "recommendation": cls._get_recommendation(severity),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    @staticmethod
    def _get_recommendation(sev: str) -> str:
        if sev == "SEVERE_ENLARGEMENT":
            return "Severe remodeling noted. Cardiology consultation and GDMT intensification strongly recommended."
        elif sev == "MODERATE_ALTERATION":
            return "Moderate structural alteration. Re-evaluate echocardiogram in 6 to 12 months."
        elif sev == "MILD_ALTERATION":
            return "Mild variation. Optimize cardiovascular risk factors and maintain blood pressure control."
        else:
            return "Normal physiological parameters within established reference limits."
