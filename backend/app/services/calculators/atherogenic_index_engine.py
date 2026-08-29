"""Atherogenic Index of Plasma (AIP) & Remnant Cholesterol Engine"""
import math
from typing import Dict, Any

class AtherogenicIndexEngine:
    @classmethod
    def calculate_aip(cls, triglycerides_mgdl: float, hdl_mgdl: float) -> Dict[str, Any]:
        tg_mmol = triglycerides_mgdl / 88.57
        hdl_mmol = hdl_mgdl / 38.67
        aip = math.log10(tg_mmol / hdl_mmol) if tg_mmol > 0 and hdl_mmol > 0 else 0.0
        return {
            "aip_value": round(aip, 3),
            "risk_category": "HIGH" if aip > 0.24 else ("INTERMEDIATE" if aip >= 0.11 else "LOW"),
            "clinical_significance": "Atherogenic particle density and dense LDL phenotype marker"
        }
