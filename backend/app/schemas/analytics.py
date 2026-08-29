from pydantic import BaseModel
from typing import List, Dict, Any

class PopulationRiskDistribution(BaseModel):
    low_risk_percent: float
    moderate_risk_percent: float
    high_risk_percent: float
    critical_risk_percent: float
    total_screened: int

class BiomarkerCohortAverage(BaseModel):
    risk_category: str
    avg_systolic_bp: float
    avg_diastolic_bp: float
    avg_bmi: float
    avg_fasting_glucose: float
    avg_total_cholesterol: float
    count: int

class AgeCohortRisk(BaseModel):
    age_group: str
    low: int
    moderate: int
    high: int
    critical: int

class AnalyticsSummaryResponse(BaseModel):
    distribution: PopulationRiskDistribution
    cohort_averages: List[BiomarkerCohortAverage]
    age_cohorts: List[AgeCohortRisk]
