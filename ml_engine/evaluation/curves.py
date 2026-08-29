import numpy as np
from typing import Dict, Any, List
from sklearn.metrics import roc_curve, precision_recall_curve
from sklearn.preprocessing import label_binarize

def generate_roc_curve_points(y_true: np.ndarray, y_prob: np.ndarray, class_names: List[str]) -> Dict[str, Any]:
    """
    Generate sampled FPR, TPR points per risk category for interactive frontend charting.
    """
    classes = np.arange(len(class_names))
    y_true_bin = label_binarize(y_true, classes=classes)
    curves = {}

    for idx, class_name in enumerate(class_names):
        if y_true_bin.shape[1] > idx:
            fpr, tpr, _ = roc_curve(y_true_bin[:, idx], y_prob[:, idx])
            # Sample down to 25 points for efficient JSON transfer
            indices = np.linspace(0, len(fpr) - 1, min(25, len(fpr)), dtype=int)
            curves[class_name] = [
                {"fpr": float(np.round(fpr[i], 3)), "tpr": float(np.round(tpr[i], 3))}
                for i in indices
            ]
    return curves
