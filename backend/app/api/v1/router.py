from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, patients, ml_models, assessments, doctors, analytics

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(patients.router)
api_router.include_router(ml_models.router)
api_router.include_router(assessments.router)
api_router.include_router(doctors.router)
api_router.include_router(analytics.router)
