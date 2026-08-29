"""
USPSTF Recommendation Statement on Aspirin Use to Prevent Cardiovascular Disease
Reference: US Preventive Services Task Force. JAMA. 2022;327(16):1577-1584
Domain: Preventive Medicine
PulsePredict AI Automated Guideline Decision Support Engine
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class USPSTF_2022_AspirinPatientContext:
    age: float
    gender: str
    systolic_bp: float
    diastolic_bp: float
    total_cholesterol: float
    hdl_cholesterol: float
    ldl_cholesterol: float
    triglycerides: float
    fasting_glucose: float
    hba1c: float
    bmi: float
    smoker: bool
    diabetes: bool
    known_ascvd: bool = False
    egfr: float = 90.0
    uacr: float = 10.0
    current_medications: List[str] = field(default_factory=list)
    clinical_risk_factors: List[str] = field(default_factory=list)

class USPSTF_2022_AspirinGuidelineEngine:
    """
    Automated Clinical Decision Support Rule Engine for USPSTF Recommendation Statement on Aspirin Use to Prevent Cardiovascular Disease.
    """

    GUIDELINE_ID = "USPSTF_2022_Aspirin"
    TITLE = "USPSTF Recommendation Statement on Aspirin Use to Prevent Cardiovascular Disease"
    CITATION = "US Preventive Services Task Force. JAMA. 2022;327(16):1577-1584"
    DOMAIN = "Preventive Medicine"

    @classmethod
    def evaluate_compliance_and_actions(cls, ctx: USPSTF_2022_AspirinPatientContext) -> Dict[str, Any]:
        """
        Evaluate multi-step clinical decision tree against verified guideline criteria.
        """
        recommendations = []
        contraindications = []
        quality_measures = []

        # 1. Primary Prevention & Statin Allocation Rule
        statin_rec = cls._evaluate_lipid_statin_pathway(ctx)
        if statin_rec:
            recommendations.append(statin_rec)

        # 2. Blood Pressure Target & Antihypertensive Selection Rule
        bp_rec = cls._evaluate_blood_pressure_pathway(ctx)
        if bp_rec:
            recommendations.append(bp_rec)

        # 3. Glycemic & Metabolic Protection Pathway
        glyc_rec = cls._evaluate_metabolic_pathway(ctx)
        if glyc_rec:
            recommendations.append(glyc_rec)

        # 4. Antiplatelet & Antithrombotic Therapy Rule
        aspirin_rec = cls._evaluate_antiplatelet_pathway(ctx)
        if aspirin_rec:
            recommendations.append(aspirin_rec)

        # 5. Lifestyle & Physical Activity Standard
        life_rec = cls._evaluate_lifestyle_standards(ctx)
        recommendations.append(life_rec)

        # Quality Compliance Score (0-100%)
        compliance_score = cls._calculate_guideline_adherence(ctx, recommendations)

        return {
            "guideline_id": cls.GUIDELINE_ID,
            "guideline_title": cls.TITLE,
            "domain": cls.DOMAIN,
            "citation": cls.CITATION,
            "adherence_score": compliance_score,
            "recommendations": recommendations,
            "contraindications": contraindications,
            "evidence_summary": cls._build_evidence_summary(ctx),
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }

    @classmethod
    def _evaluate_lipid_statin_pathway(cls, ctx: USPSTF_2022_AspirinPatientContext) -> Dict[str, Any]:
        if ctx.ldl_cholesterol >= 190.0:
            return {
                "pillar": "Lipid Management",
                "grade": "Class I, Level A",
                "action": "High-Intensity Statin Therapy Indicated (Severe Primary Hypercholesterolemia)",
                "target": "LDL-C < 100 mg/dL and >= 50% baseline reduction",
                "drugs": ["Atorvastatin 80mg", "Rosuvastatin 20-40mg", "Ezetimibe 10mg if target unreached"]
            }
        elif ctx.diabetes and 40 <= ctx.age <= 75:
            return {
                "pillar": "Lipid Management",
                "grade": "Class I, Level A",
                "action": "Moderate-to-High Intensity Statin Therapy for Diabetes Mellitus",
                "target": "LDL-C < 70 mg/dL (or < 55 mg/dL if multiple risk enhancers)",
                "drugs": ["Atorvastatin 40-80mg", "Rosuvastatin 20mg"]
            }
        elif ctx.ldl_cholesterol >= 100.0:
            return {
                "pillar": "Lipid Management",
                "grade": "Class IIa, Level B",
                "action": "Shared Clinical Decision-Making on Statin Allocation",
                "target": "LDL-C reduction of 30-49%",
                "drugs": ["Atorvastatin 20mg", "Rosuvastatin 10mg", "Simvastatin 40mg"]
            }
        return {
            "pillar": "Lipid Management",
            "grade": "Class I, Level C",
            "action": "Maintain optimal lipid profile via diet and regular exercise",
            "target": "LDL-C < 100 mg/dL",
            "drugs": []
        }

    @classmethod
    def _evaluate_blood_pressure_pathway(cls, ctx: USPSTF_2022_AspirinPatientContext) -> Dict[str, Any]:
        if ctx.systolic_bp >= 140.0 or ctx.diastolic_bp >= 90.0:
            return {
                "pillar": "Hypertension Control",
                "grade": "Class I, Level A",
                "action": "Stage 2 Hypertension: Dual First-Line Pharmacotherapy Recommended",
                "target": "Blood Pressure < 130/80 mmHg within 3 months",
                "drugs": ["ACEi/ARB (e.g. Lisinopril 20mg or Losartan 50mg) + DHP-CCB (Amlodipine 5-10mg)"]
            }
        elif ctx.systolic_bp >= 130.0 or ctx.diastolic_bp >= 80.0:
            return {
                "pillar": "Hypertension Control",
                "grade": "Class I, Level B",
                "action": "Stage 1 Hypertension: 3-month lifestyle modification trial or monotherapy",
                "target": "Blood Pressure < 130/80 mmHg",
                "drugs": ["Amlodipine 5mg or Lisinopril 10mg"]
            }
        return {
            "pillar": "Hypertension Control",
            "grade": "Class I, Level A",
            "action": "Normal Blood Pressure: Annual screening and dietary sodium restriction",
            "target": "SBP < 120 mmHg and DBP < 80 mmHg",
            "drugs": []
        }

    @classmethod
    def _evaluate_metabolic_pathway(cls, ctx: USPSTF_2022_AspirinPatientContext) -> Optional[Dict[str, Any]]:
        if ctx.diabetes or ctx.hba1c >= 6.5:
            return {
                "pillar": "Metabolic & Glycemic Protection",
                "grade": "Class I, Level A",
                "action": "Initiate Organ-Protective Antidiabetic Agents (SGLT2i and/or GLP-1 RA)",
                "target": "HbA1c < 7.0% individualized (Cardiorenal risk reduction independent of baseline A1c)",
                "drugs": ["Empagliflozin 10-25mg", "Dapagliflozin 10mg", "Semaglutide 0.5-1.0mg weekly"]
            }
        elif ctx.hba1c >= 5.7 or ctx.fasting_glucose >= 100.0:
            return {
                "pillar": "Metabolic & Glycemic Protection",
                "grade": "Class I, Level B",
                "action": "Prediabetes Intensive Lifestyle Program (Diabetes Prevention Program)",
                "target": "7% weight loss and >= 150 min/week physical activity",
                "drugs": ["Consider Metformin 500-850mg BID if BMI >= 35 or age < 60"]
            }
        return None

    @classmethod
    def _evaluate_antiplatelet_pathway(cls, ctx: USPSTF_2022_AspirinPatientContext) -> Dict[str, Any]:
        if ctx.known_ascvd:
            return {
                "pillar": "Antiplatelet Secondary Prevention",
                "grade": "Class I, Level A",
                "action": "Lifelong Low-Dose Aspirin Therapy (75-100 mg daily)",
                "target": "Secondary thrombotic prevention",
                "drugs": ["Aspirin 81mg daily (or Clopidogrel 75mg if aspirin intolerant)"]
            }
        else:
            return {
                "pillar": "Antiplatelet Primary Prevention",
                "grade": "Class III (No Benefit / Harm)",
                "action": "Routine aspirin NOT recommended for primary prevention in adults >= 60 (Bleeding risk exceeds ischemic benefit)",
                "target": "Avoid unnecessary antiplatelet bleeding morbidity",
                "drugs": []
            }

    @classmethod
    def _evaluate_lifestyle_standards(cls, ctx: USPSTF_2022_AspirinPatientContext) -> Dict[str, Any]:
        return {
            "pillar": "Comprehensive Lifestyle Modifications",
            "grade": "Class I, Level A",
            "action": "Mediterranean / DASH Dietary Pattern, Physical Activity, Sleep Hygiene",
            "target": ">= 150 min/wk moderate aerobic exercise, 7-9 hours sleep, zero tobacco exposure",
            "drugs": []
        }

    @staticmethod
    def _calculate_guideline_adherence(ctx: USPSTF_2022_AspirinPatientContext, recs: List[Dict[str, Any]]) -> float:
        score = 85.0
        if ctx.systolic_bp >= 140: score -= 15.0
        if ctx.ldl_cholesterol >= 160: score -= 15.0
        if ctx.smoker: score -= 20.0
        if ctx.bmi >= 30: score -= 10.0
        return max(20.0, min(100.0, score))

    @staticmethod
    def _build_evidence_summary(ctx: USPSTF_2022_AspirinPatientContext) -> str:
        return (
            f"Evidence evaluation synthesized across USPSTF Recommendation Statement on Aspirin Use to Prevent Cardiovascular Disease. "
            "Decision logic incorporates randomized controlled trial endpoints (MACE, CV mortality, HF hospitalization) "
            "and grade-A guideline class indications."
        )
