from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models.base import TimestampMixin, GUID
from app.models.enums import DatasetSplit

class MLModelRegistry(Base, TimestampMixin):
    __tablename__ = "ml_models"

    model_name = Column(String(100), nullable=False, index=True)
    model_version = Column(String(50), nullable=False, index=True)
    artifact_path = Column(String(500), nullable=False)
    hyperparameters = Column(JSON, default=dict, nullable=False)
    is_active_for_inference = Column(Boolean, default=True, nullable=False)
    trained_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    metrics = relationship("ModelMetrics", back_populates="model", cascade="all, delete-orphan")

class ModelMetrics(Base, TimestampMixin):
    __tablename__ = "model_metrics"

    model_id = Column(GUID(), ForeignKey("ml_models.id", ondelete="CASCADE"), nullable=False, index=True)
    dataset_split = Column(SQLEnum(DatasetSplit), default=DatasetSplit.TEST, nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    roc_auc = Column(Float, nullable=False)
    confusion_matrix = Column(JSON, default=dict, nullable=False)
    roc_curve_points = Column(JSON, default=dict, nullable=False)
    feature_importances = Column(JSON, default=dict, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    model = relationship("MLModelRegistry", back_populates="metrics")
