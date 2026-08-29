from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

    PROJECT_NAME: str = "PulsePredict AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "change_this_to_a_cryptographically_secure_random_key_in_production_min32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15
    
    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000", "http://127.0.0.1:3000"]

    # PostgreSQL
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "pulseadmin"
    POSTGRES_PASSWORD: str = "pulseadmin_secure_pw_2026"
    POSTGRES_DB: str = "pulsepredict_db"
    
    DATABASE_URL: str = "postgresql+asyncpg://pulseadmin:pulseadmin_secure_pw_2026@localhost:5432/pulsepredict_db"
    SYNC_DATABASE_URL: str = "postgresql+psycopg2://pulseadmin:pulseadmin_secure_pw_2026@localhost:5432/pulsepredict_db"
    
    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ML Paths
    MODEL_REGISTRY_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml_engine", "saved_models")
    DEFAULT_MODEL_VERSION: str = "v1.0.0"
    ENABLE_SHAP_EXPLAINABILITY: bool = True

    # Storage
    STORAGE_ROOT: str = "./storage"
    PDF_REPORTS_DIR: str = "./storage/reports"

settings = Settings()
