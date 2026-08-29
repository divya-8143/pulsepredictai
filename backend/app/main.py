from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import AppException
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    Enterprise AI/ML Health Risk Assessment & Decision Support Platform.
    
    * Multi-model risk prediction (Logistic Regression, Random Forest, XGBoost)
    * Role-Based Access Control (Patient, Doctor, Admin)
    * Longitudinal biomarker tracking, SHAP explainability & clinical PDF reporting.
    
    **Disclaimer**: Designed for clinical risk assessment and monitoring. Does NOT provide definitive medical diagnoses.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Timing & Diagnostic Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response

# Global Exception Handler
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
    """System health & readiness probe."""
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "disclaimer": "For clinical risk assessment & monitoring only. Not a medical diagnosis."
    }

# Mount v1 REST APIs
app.include_router(api_router, prefix=settings.API_V1_STR)
