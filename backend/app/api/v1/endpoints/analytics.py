from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import require_doctor
from app.models.user import User
from app.schemas.analytics import AnalyticsSummaryResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Population Risk Analytics"])

@router.get("/population-risk", response_model=AnalyticsSummaryResponse)
async def get_population_risk_analytics(
    current_user: User = Depends(require_doctor),
    db: AsyncSession = Depends(get_db)
):
    """Population health risk distribution, age cohorts, and biomarker averages."""
    return await AnalyticsService.get_population_analytics(db)
