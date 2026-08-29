from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.enums import DatasetSplit

class MLModelRegistry(Base, TimestampMixin):
    __tablename__ = "ml_models"

    model_name = Column(String(100), nullable=False, index=True)  # LogisticRegression, RandomForest, XGBoost
    model_version = Column(String(50), nullable=False, index=True) # v1.0.0
    artifact_path = Column(String(500), nullable=False)
    hyperparameters = Column(JSONB, default=dict, nullable=False)
    is_active_for_inference = Column(Boolean, default=True, nullable=False)
    trained_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    metrics = relationship("ModelMetrics", back_populates="model", cascade="all, delete-orphan")

class ModelMetrics(Base, TimestampMixin):
    __tablename__ = "model_metrics"

    model_id = Column(UUID(as_uuid=True), ForeignKey("ml_models.id", ondelete="CASCADE"), nullable=False, index=True)
    dataset_split = Column(SQLEnum(DatasetSplit), default=DatasetSplit.TEST, nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    roc_auc = Column(Float, nullable=False)
    confusion_matrix = Column(JSONB, default=dict, nullable=False)
    roc_curve_points = Column(JSONB, default=dict, nullable=False)
    feature_importances = Column(JSONB, default=dict, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    model = relationship("MLModelRegistry", back_populates="metrics")
