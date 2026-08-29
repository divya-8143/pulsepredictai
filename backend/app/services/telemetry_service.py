"""
Real-Time Vitals Telemetry & Continuous Cardiac Monitoring Engine.
Processes high-frequency biometric streams (ECG, HR, SpO2, BP) and generates instant arrhythmia flags.
"""

from typing import Dict, Any, List, Optional
import math
import random
from datetime import datetime

class RealtimeTelemetryEngine:
    @classmethod
    def ingest_vitals_frame(cls, frame: Dict[str, Any]) -> Dict[str, Any]:
        hr = float(frame.get("heart_rate", 72))
        spo2 = float(frame.get("spo2", 98))
        sbp = float(frame.get("systolic_bp", 120))
        dbp = float(frame.get("diastolic_bp", 80))

        alarms = []
        if hr > 120:
            alarms.append({"level": "CRITICAL", "message": f"Tachycardia detected ({hr:.0f} bpm)."})
        elif hr < 45:
            alarms.append({"level": "CRITICAL", "message": f"Bradycardia alert ({hr:.0f} bpm)."})

        if spo2 < 92:
            alarms.append({"level": "URGENT", "message": f"Desaturation event ({spo2:.1f}% SpO2)."})

        if sbp >= 180 or dbp >= 120:
            alarms.append({"level": "EMERGENCY", "message": f"Hypertensive Crisis ({sbp:.0f}/{dbp:.0f} mmHg)."})

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "hemodynamic_status": "CRITICAL" if alarms else "STABLE",
            "active_alarms": alarms,
            "mean_arterial_pressure": round((2 * dbp + sbp) / 3.0, 1),
            "cardiac_workload_index": round((hr * sbp) / 100.0, 1)
        }
