from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ModelSummary(BaseModel):
    model_name: str
    version: str
    status: str
    type: str

class ModelPerformanceMetricsResponse(BaseModel):
    model_name: str
    version: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: List[List[int]]
    roc_curve: Dict[str, List[Dict[str, float]]]
    class_labels: List[str]
