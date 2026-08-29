from typing import Dict, Any, List, Tuple
from app.schemas.assessment import HealthDataInput

class BiomarkerAnomalyDetectionService:
    """
    Advanced multi-biomarker physiological coherence and laboratory discrepancy analyzer.
    Validates biochemical equations, hemodynamic laws, and metabolic correlations.
    """

    @classmethod
    def analyze_physiological_coherence(cls, data: HealthDataInput) -> Dict[str, Any]:
        discrepancies: List[Dict[str, str]] = []
        severity_score = 0  # 0 to 100

        # 1. Hemodynamic Pulse Pressure Coherence
        pulse_pressure = data.systolic_bp - data.diastolic_bp
        if pulse_pressure < 15.0:
            discrepancies.append({
                "type": "HEMODYNAMIC_INCOHERENCE",
                "severity": "HIGH",
                "parameter": "Blood Pressure",
                "message": f"Severely narrowed pulse pressure ({pulse_pressure} mmHg). SBP and DBP difference must exceed 15 mmHg."
            })
            severity_score += 35
        elif pulse_pressure > 110.0:
            discrepancies.append({
                "type": "HEMODYNAMIC_ALERT",
                "severity": "MODERATE",
                "parameter": "Blood Pressure",
                "message": f"Widened pulse pressure ({pulse_pressure} mmHg) suggests severe arterial stiffness or aortic regurgitation."
            })
            severity_score += 15

        # 2. Glycemic Incoherence (Fasting Glucose vs HbA1c)
        eag = 28.7 * data.hba1c - 46.7
        glucose_diff = abs(data.fasting_glucose - eag)
        if data.fasting_glucose > 220.0 and data.hba1c < 5.4:
            discrepancies.append({
                "type": "GLYCEMIC_DISCREPANCY",
                "severity": "HIGH",
                "parameter": "Glucose / HbA1c",
                "message": f"Acute hyperglycemia ({data.fasting_glucose} mg/dL) with normal HbA1c ({data.hba1c}%) indicates acute stress or lab error."
            })
            severity_score += 30
        elif data.fasting_glucose < 70.0 and data.hba1c > 8.0:
            discrepancies.append({
                "type": "GLYCEMIC_DISCREPANCY",
                "severity": "MODERATE",
                "parameter": "Glucose / HbA1c",
                "message": f"Hypoglycemic fasting glucose ({data.fasting_glucose} mg/dL) with high chronic HbA1c ({data.hba1c}%) suggests medication excess or rebound."
            })
            severity_score += 20

        # 3. Lipid Partition & Friedewald Verification
        calculated_tc = data.hdl_cholesterol + data.ldl_cholesterol + (data.triglycerides / 5.0)
        tc_discrepancy = abs(data.total_cholesterol - calculated_tc)
        if tc_discrepancy > 40.0 and data.triglycerides < 400.0:
            discrepancies.append({
                "type": "LIPID_FRACTION_MISMATCH",
                "severity": "MODERATE",
                "parameter": "Lipid Panel",
                "message": f"Total cholesterol ({data.total_cholesterol} mg/dL) deviates from sum of fractions ({calculated_tc:.1f} mg/dL) by {tc_discrepancy:.1f} mg/dL."
            })
            severity_score += 15

        is_plausible = severity_score < 40
        return {
            "is_physiologically_coherent": is_plausible,
            "discrepancy_count": len(discrepancies),
            "anomaly_severity_index": min(100, severity_score),
            "coherence_tier": "OPTIMAL" if severity_score == 0 else ("SUSPICIOUS" if is_plausible else "CRITICAL_INCOHERENCE"),
            "discrepancies": discrepancies,
            "recommended_action": "Proceed with inference" if is_plausible else "Require user or clinical re-verification of biometrics before finalizing assessment."
        }
