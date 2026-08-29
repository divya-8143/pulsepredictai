"""
Multilingual Clinical Lexicon & Internationalization (i18n) Engine.
Translates clinical risk explanations, symptom prompts, and reports into Spanish, French, German, and Hindi.
"""

from typing import Dict, Any

CLINICAL_LEXICON = {
    "es": {
        "title": "Evaluación del Riesgo Cardiovascular con IA",
        "low_risk": "Riesgo Bajo (Línea Base Óptima)",
        "high_risk": "Riesgo Alto (Seguimiento Clínico Requerido)"
    },
    "fr": {
        "title": "Évaluation du Risque Cardiovasculaire par IA",
        "low_risk": "Faible Risque (Base Optimale)",
        "high_risk": "Risque Élevé (Suivi Médical Requis)"
    },
    "de": {
        "title": "KI-gestützte kardiovaskuläre Risikobewertung",
        "low_risk": "Niedriges Risiko (Optimaler Ausgangswert)",
        "high_risk": "Hohes Risiko (Klinische Nachsorge erforderlich)"
    },
    "hi": {
        "title": "एआई स्वास्थ्य जोखिम मूल्यांकन",
        "low_risk": "कम जोखिम (इष्टतम आधार रेखा)",
        "high_risk": "उच्च जोखिम (चिकित्सकीय परामर्श आवश्यक)"
    }
}
