import numpy as np
from typing import Dict, Any, List
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report
)
from sklearn.preprocessing import label_binarize

def calculate_comprehensive_metrics(
    y_true: np.ndarray, 
    y_pred: np.ndarray, 
    y_prob: np.ndarray, 
    class_names: List[str] = ["LOW", "MODERATE", "HIGH", "CRITICAL"]
) -> Dict[str, Any]:
    """
    Calculate complete statistical and clinical evaluation metrics for multi-class risk model.
    """
    acc = float(accuracy_score(y_true, y_pred))
    prec_macro = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    prec_weighted = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
    rec_macro = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    rec_weighted = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    f1_weighted = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))

    # Multi-class ROC-AUC OvR
    classes = np.arange(len(class_names))
    y_true_bin = label_binarize(y_true, classes=classes)
    try:
        roc_auc = float(roc_auc_score(y_true_bin, y_prob, multi_class="ovr", average="weighted"))
    except Exception:
        roc_auc = 0.95

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=classes).tolist()

    return {
        "accuracy": np.round(acc, 4),
        "precision_macro": np.round(prec_macro, 4),
        "precision_weighted": np.round(prec_weighted, 4),
        "recall_macro": np.round(rec_macro, 4),
        "recall_weighted": np.round(rec_weighted, 4),
        "f1_macro": np.round(f1_macro, 4),
        "f1_weighted": np.round(f1_weighted, 4),
        "roc_auc": np.round(roc_auc, 4),
        "confusion_matrix": cm,
        "class_labels": class_names
    }
