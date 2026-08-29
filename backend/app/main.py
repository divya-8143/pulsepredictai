from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import AppException
from app.core.database import async_engine, Base, AsyncSessionLocal
from app.api.v1.router import api_router
from ml_engine.training.registry import ModelRegistryService
import app.models  # ensure all models registered

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database schemas...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Initializing Machine Learning Registry...")
    ModelRegistryService.get_instance()

    from scripts.seed_db import seed_database
    try:
        await seed_database()
    except Exception as e:
        logger.warning(f"Auto-seed notification: {e}")
        
    yield
    logger.info("Shutting down PulsePredict AI API service.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    Enterprise AI/ML Health Risk Assessment & Decision Support Platform.
    * Multi-model risk prediction (Logistic Regression, Random Forest, XGBoost)
    * Role-Based Access Control (Patient, Doctor, Admin)
    * Longitudinal biomarker tracking, SHAP explainability & clinical PDF reporting.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"Application exception: {exc.detail} | Code: {exc.error_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.error_code,
            "message": exc.detail,
            "extra": exc.extra
        }
    )

@app.get("/health", tags=["System Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "disclaimer": "For clinical risk assessment & monitoring only. Not a medical diagnosis."
    }

app.include_router(api_router, prefix=settings.API_V1_STR)
