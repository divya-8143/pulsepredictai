import os
import glob
from typing import Dict, Any, Optional, List
from ml_engine.config import SAVED_MODELS_DIR
from ml_engine.models.base_model import BaseHealthRiskModel
from ml_engine.models.logistic_regression import LogisticRegressionRiskModel
from ml_engine.models.random_forest import RandomForestRiskModel
from ml_engine.models.xgboost_model import XGBoostRiskModel
from ml_engine.models.ensemble import CalibratedEnsembleRiskModel

class ModelRegistryService:
    _instance = None
    _loaded_models: Dict[str, BaseHealthRiskModel] = {}
    _ensemble: Optional[CalibratedEnsembleRiskModel] = None

    @classmethod
    def get_instance(cls) -> "ModelRegistryService":
        if cls._instance is None:
            cls._instance = ModelRegistryService()
            cls._instance.initialize_models()
        return cls._instance

    def initialize_models(self):
        print(f"Loading ML Model artifacts from {SAVED_MODELS_DIR}...")
        os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
        
        lr_path = os.path.join(SAVED_MODELS_DIR, "logisticregression_v1.0.0.joblib")
        rf_path = os.path.join(SAVED_MODELS_DIR, "randomforest_v1.0.0.joblib")
        xgb_path = os.path.join(SAVED_MODELS_DIR, "xgboost_v1.0.0.joblib")

        models = {}
        if os.path.exists(lr_path):
            models["LogisticRegression"] = LogisticRegressionRiskModel.load(lr_path)
        if os.path.exists(rf_path):
            models["RandomForest"] = RandomForestRiskModel.load(rf_path)
        if os.path.exists(xgb_path):
            models["XGBoost"] = XGBoostRiskModel.load(xgb_path)

        self._loaded_models = models
        if models:
            self._ensemble = CalibratedEnsembleRiskModel(models=models, version="v1.0.0")
            print(f"Ensemble loaded successfully with {len(models)} base classifiers.")
        else:
            print("Warning: No model artifacts found in registry path.")

    def get_ensemble(self) -> CalibratedEnsembleRiskModel:
        if self._ensemble is None:
            self.initialize_models()
        if self._ensemble is None:
            raise RuntimeError("Model registry could not initialize ensemble model.")
        return self._ensemble

    def get_model(self, model_name: str) -> Optional[BaseHealthRiskModel]:
        return self._loaded_models.get(model_name)

    def list_models_info(self) -> List[Dict[str, Any]]:
        info = []
        for name, m in self._loaded_models.items():
            info.append({
                "model_name": name,
                "version": m.version,
                "status": "ACTIVE",
                "type": "CLASSIFICATION_RISK"
            })
        if self._ensemble:
            info.append({
                "model_name": "CalibratedEnsemble",
                "version": self._ensemble.version,
                "status": "PRIMARY_ACTIVE",
                "type": "SOFT_VOTING_ENSEMBLE"
            })
        return info
