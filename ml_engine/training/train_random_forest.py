import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from sklearn.preprocessing import label_binarize

from ml_engine.config import RAW_DATA_PATH, SAVED_MODELS_DIR, RANDOM_SEED, TARGET_COLUMN
from ml_engine.datasets.generator import generate_synthetic_clinical_dataset
from ml_engine.models.random_forest import RandomForestRiskModel

def train_and_save_random_forest():
    if not os.path.exists(RAW_DATA_PATH):
        generate_synthetic_clinical_dataset()

    df = pd.read_csv(RAW_DATA_PATH)
    X = df.drop(columns=["risk_score", "risk_category_encoded"])
    y = df[TARGET_COLUMN].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    print("Training Random Forest Classifier Model...")
    model = RandomForestRiskModel(version="v1.0.0", n_estimators=250, max_depth=12)
    model.fit(X_train, y_train)

    y_pred = model.pipeline.predict(X_test)
    y_prob = model.predict_proba(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    
    classes = np.unique(y)
    y_test_bin = label_binarize(y_test, classes=classes)
    roc_auc = roc_auc_score(y_test_bin, y_prob, multi_class="ovr", average="weighted")

    print(f"Random Forest Metrics -> Accuracy: {acc:.4f} | F1: {f1:.4f} | ROC-AUC: {roc_auc:.4f}")
    save_path = model.save(SAVED_MODELS_DIR)
    return save_path

if __name__ == "__main__":
    train_and_save_random_forest()
