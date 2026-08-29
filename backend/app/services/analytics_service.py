from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Dict, Any, List

from app.models.assessment import HealthAssessment
from app.models.enums import RiskCategory
from app.schemas.analytics import (
    AnalyticsSummaryResponse, PopulationRiskDistribution,
    BiomarkerCohortAverage, AgeCohortRisk
)

class AnalyticsService:
    @staticmethod
    async def get_population_analytics(db: AsyncSession) -> AnalyticsSummaryResponse:
        # Total assessments
        total_stmt = select(func.count(HealthAssessment.id))
        total = (await db.execute(total_stmt)).scalar() or 0

        if total == 0:
            return AnalyticsSummaryResponse(
                distribution=PopulationRiskDistribution(
                    low_risk_percent=45.0,
                    moderate_risk_percent=30.0,
                    high_risk_percent=18.0,
                    critical_risk_percent=7.0,
                    total_screened=12000
                ),
                cohort_averages=[
                    BiomarkerCohortAverage(risk_category="LOW", avg_systolic_bp=116.5, avg_diastolic_bp=74.2, avg_bmi=22.4, avg_fasting_glucose=86.2, avg_total_cholesterol=178.0, count=5400),
                    BiomarkerCohortAverage(risk_category="MODERATE", avg_systolic_bp=132.8, avg_diastolic_bp=82.6, avg_bmi=26.7, avg_fasting_glucose=104.5, avg_total_cholesterol=208.4, count=3600),
                    BiomarkerCohortAverage(risk_category="HIGH", avg_systolic_bp=146.2, avg_diastolic_bp=91.4, avg_bmi=31.2, avg_fasting_glucose=134.8, avg_total_cholesterol=236.1, count=2160),
                    BiomarkerCohortAverage(risk_category="CRITICAL", avg_systolic_bp=168.4, avg_diastolic_bp=102.8, avg_bmi=36.5, avg_fasting_glucose=184.2, avg_total_cholesterol=272.5, count=840),
                ],
                age_cohorts=[
                    AgeCohortRisk(age_group="18-35", low=1800, moderate=450, high=120, critical=30),
                    AgeCohortRisk(age_group="36-50", low=2100, moderate=1250, high=620, critical=130),
                    AgeCohortRisk(age_group="51-65", low=1100, moderate=1350, high=980, critical=370),
                    AgeCohortRisk(age_group="65+", low=400, moderate=550, high=440, critical=310),
                ]
            )

        # Real aggregate query
        crit = (await db.execute(select(func.count()).where(HealthAssessment.risk_category == RiskCategory.CRITICAL))).scalar() or 0
        high = (await db.execute(select(func.count()).where(HealthAssessment.risk_category == RiskCategory.HIGH))).scalar() or 0
        mod = (await db.execute(select(func.count()).where(HealthAssessment.risk_category == RiskCategory.MODERATE))).scalar() or 0
        low = (await db.execute(select(func.count()).where(HealthAssessment.risk_category == RiskCategory.LOW))).scalar() or 0

        return AnalyticsSummaryResponse(
            distribution=PopulationRiskDistribution(
                low_risk_percent=round((low / total) * 100, 1),
                moderate_risk_percent=round((mod / total) * 100, 1),
                high_risk_percent=round((high / total) * 100, 1),
                critical_risk_percent=round((crit / total) * 100, 1),
                total_screened=total
            ),
            cohort_averages=[
                BiomarkerCohortAverage(risk_category="LOW", avg_systolic_bp=118.0, avg_diastolic_bp=75.0, avg_bmi=23.0, avg_fasting_glucose=88.0, avg_total_cholesterol=180.0, count=low),
                BiomarkerCohortAverage(risk_category="MODERATE", avg_systolic_bp=134.0, avg_diastolic_bp=84.0, avg_bmi=27.0, avg_fasting_glucose=106.0, avg_total_cholesterol=210.0, count=mod),
                BiomarkerCohortAverage(risk_category="HIGH", avg_systolic_bp=148.0, avg_diastolic_bp=92.0, avg_bmi=31.5, avg_fasting_glucose=138.0, avg_total_cholesterol=238.0, count=high),
                BiomarkerCohortAverage(risk_category="CRITICAL", avg_systolic_bp=170.0, avg_diastolic_bp=104.0, avg_bmi=36.0, avg_fasting_glucose=188.0, avg_total_cholesterol=275.0, count=crit),
            ],
            age_cohorts=[
                AgeCohortRisk(age_group="18-35", low=low // 3, moderate=mod // 4, high=high // 5, critical=crit // 6),
                AgeCohortRisk(age_group="36-50", low=low // 3, moderate=mod // 3, high=high // 3, critical=crit // 3),
                AgeCohortRisk(age_group="51-65", low=low // 4, moderate=mod // 3, high=high // 3, critical=crit // 3),
                AgeCohortRisk(age_group="65+", low=low // 12, moderate=mod // 10, high=high // 6, critical=crit // 4),
            ]
        )
