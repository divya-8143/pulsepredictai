from typing import Dict, Any, List, Optional
from datetime import datetime

class ClinicalEscalationService:
    """
    Automated longitudinal risk delta tracking and critical patient alert routing.
    Detects accelerated deterioration (>15% risk surge or Critical Tier >=35%).
    """

    @classmethod
    def evaluate_escalation_triggers(
        cls,
        current_assessment: Dict[str, Any],
        historical_assessments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        current_score = current_assessment.get("overall_risk_score", 0.0)
        current_tier = current_assessment.get("risk_category", "LOW")
        escalation_reasons = []
        is_critical_escalation = False

        if current_score >= 35.0 or current_tier in ["CRITICAL", "HIGH_RISK"]:
            is_critical_escalation = True
            escalation_reasons.append(
                f"Critical risk threshold exceeded ({current_score:.1f}%). Mandates priority physician review within 24 hours."
            )

        if historical_assessments:
            prev_assessment = historical_assessments[0]
            prev_score = prev_assessment.get("overall_risk_score", current_score)
            delta = current_score - prev_score
            if delta >= 15.0:
                is_critical_escalation = True
                escalation_reasons.append(
                    f"Rapid risk acceleration detected: +{delta:.1f}% surge since previous evaluation."
                )

        sbp = current_assessment.get("systolic_bp", 120.0)
        dbp = current_assessment.get("diastolic_bp", 80.0)
        if sbp >= 180.0 or dbp >= 120.0:
            is_critical_escalation = True
            escalation_reasons.append(
                f"Hypertensive Urgency threshold reached ({sbp:.0f}/{dbp:.0f} mmHg). Immediate clinical triaging required."
            )

        return {
            "requires_escalation": is_critical_escalation,
            "escalation_priority": "EMERGENT_STAT" if sbp >= 180.0 else ("HIGH_PRIORITY_24H" if is_critical_escalation else "ROUTINE"),
            "escalation_reasons": escalation_reasons,
            "dual_physician_signoff_required": is_critical_escalation and current_score >= 45.0,
            "escalated_at": datetime.utcnow().isoformat() + "Z"
        }
