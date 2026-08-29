"""
Post-PCI Dual Antiplatelet Therapy (DAPT) Ischemic vs Bleeding De-escalation
Specialty: Cardiology
PulsePredict AI Standardized Clinical Decision Pathway Engine
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PostPciDaptDurationContext:
    patient_id: str
    age: float
    gender: str
    biomarker_primary: float
    biomarker_secondary: float
    current_line_of_therapy: int = 1
    intolerances: List[str] = field(default_factory=list)
    comorbidities: List[str] = field(default_factory=list)

class PostPciDaptDurationProtocolEngine:
    """
    Standardized Protocol Implementation for Post-PCI Dual Antiplatelet Therapy (DAPT) Ischemic vs Bleeding De-escalation.
    """

    PROTOCOL_NAME = "Post-PCI Dual Antiplatelet Therapy (DAPT) Ischemic vs Bleeding De-escalation"
    SPECIALTY = "Cardiology"

    @classmethod
    def execute_protocol(cls, ctx: PostPciDaptDurationContext) -> Dict[str, Any]:
        """
        Evaluate patient clinical criteria through multi-tier stepped therapy.
        """
        current_step = cls._determine_step(ctx)
        dosing_plan = cls._generate_dosing_plan(current_step, ctx)
        monitoring_schedule = cls._generate_monitoring_schedule(current_step, ctx)
        safety_checks = cls._perform_safety_checks(ctx)

        return {
            "protocol_name": cls.PROTOCOL_NAME,
            "specialty": cls.SPECIALTY,
            "patient_id": ctx.patient_id,
            "recommended_step": current_step,
            "dosing_plan": dosing_plan,
            "monitoring_schedule": monitoring_schedule,
            "safety_alerts": safety_checks,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    @classmethod
    def _determine_step(cls, ctx: PostPciDaptDurationContext) -> int:
        if ctx.current_line_of_therapy >= 3 or ctx.biomarker_primary >= 160.0:
            return 3
        elif ctx.current_line_of_therapy >= 2 or ctx.biomarker_primary >= 130.0:
            return 2
        return 1

    @classmethod
    def _generate_dosing_plan(cls, step: int, ctx: PostPciDaptDurationContext) -> List[Dict[str, str]]:
        if step == 3:
            return [
                {"phase": "Step 3 (Intensified)", "medication": "Triple Combination / Target Dose", "frequency": "Daily", "notes": "Specialist co-management suggested."},
                {"phase": "Add-On", "medication": "Adjunctive Target Organ Protective Agent", "frequency": "Daily", "notes": "Monitor renal and hepatic labs."}
            ]
        elif step == 2:
            return [
                {"phase": "Step 2 (Dual Therapy)", "medication": "First-Line Agent (High Dose) + Second-Line Agent", "frequency": "Daily", "notes": "Evaluate efficacy at 6-8 weeks."}
            ]
        else:
            return [
                {"phase": "Step 1 (Initial)", "medication": "First-Line Monotherapy Standard Titration", "frequency": "Daily", "notes": "Initiate lifestyle foundation concomitantly."}
            ]

    @classmethod
    def _generate_monitoring_schedule(cls, step: int, ctx: PostPciDaptDurationContext) -> List[Dict[str, str]]:
        return [
            {"interval": "2 Weeks", "check": "Safety labs (Serum Electrolytes, Creatinine, eGFR)", "target": "eGFR drop < 30%"},
            {"interval": "6-8 Weeks", "check": "Target Biomarker Level & Tolerance Review", "target": "Goal achievement"},
            {"interval": "6 Months", "check": "Long-Term Adherence & Cardiovascular Risk Re-Evaluation", "target": "Sustained stability"}
        ]

    @classmethod
    def _perform_safety_checks(cls, ctx: PostPciDaptDurationContext) -> List[str]:
        alerts = []
        if "renal" in " ".join(ctx.comorbidities).lower() and ctx.biomarker_secondary < 30.0:
            alerts.append("Severe Renal Impairment (eGFR < 30): Dose titration requires nephrology clearance.")
        if "hypotension" in " ".join(ctx.comorbidities).lower():
            alerts.append("Orthostatic liability noted; check standing blood pressure.")
        return alerts
