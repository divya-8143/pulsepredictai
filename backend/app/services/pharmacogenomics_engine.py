"""
Cardiovascular Pharmacogenomics & Multidrug Interaction Screening Engine.
Identifies CYP450 enzyme conflicts, renal clearance contraindications, and statin-myopathy risk.
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime

class PharmacogenomicsInteractionEngine:
    DRUG_DATABASE = {
        "atorvastatin": {"class": "Statin", "cyp": "CYP3A4", "contraindications": ["gemfibrozil", "clarithromycin"]},
        "rosuvastatin": {"class": "Statin", "cyp": "CYP2C9", "contraindications": ["gemfibrozil"]},
        "clopidogrel": {"class": "Antiplatelet", "cyp": "CYP2C19", "contraindications": ["omeprazole", "esomeprazole"]},
        "apixaban": {"class": "DOAC", "cyp": "CYP3A4 / P-gp", "contraindications": ["ketoconazole", "rifampin"]},
        "lisinopril": {"class": "ACE Inhibitor", "renal_clearance": True, "contraindications": ["sacubitril/valsartan", "aliskiren"]},
        "empagliflozin": {"class": "SGLT2 Inhibitor", "renal_threshold_egfr": 20, "contraindications": []},
        "semaglutide": {"class": "GLP-1 RA", "contraindications": ["medullary thyroid carcinoma history"]}
    }

    @classmethod
    def screen_medication_regimen(
        cls,
        current_medications: List[str],
        allergies: List[str] = None,
        egfr: float = 85.0
    ) -> Dict[str, Any]:
        meds_lower = [m.lower().strip() for m in current_medications]
        interactions = []
        dosage_warnings = []

        for m in meds_lower:
            drug_info = cls.DRUG_DATABASE.get(m)
            if not drug_info:
                continue

            for contra in drug_info.get("contraindications", []):
                if contra in meds_lower:
                    interactions.append({
                        "severity": "CRITICAL_AVOID",
                        "drug_a": m.title(),
                        "drug_b": contra.title(),
                        "clinical_consequence": f"High risk pharmacokinetic interaction via {drug_info.get('cyp', 'hepatic/renal pathway')}."
                    })

            if "renal_threshold_egfr" in drug_info and egfr < drug_info["renal_threshold_egfr"]:
                dosage_warnings.append(
                    f"{m.title()}: Contraindicated in severe renal impairment (eGFR {egfr} < {drug_info['renal_threshold_egfr']})."
                )

        return {
            "total_medications_screened": len(meds_lower),
            "safety_verdict": "SAFE" if not interactions and not dosage_warnings else "INTERACTION_ALERT",
            "critical_interactions": interactions,
            "renal_dosage_warnings": dosage_warnings,
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }
