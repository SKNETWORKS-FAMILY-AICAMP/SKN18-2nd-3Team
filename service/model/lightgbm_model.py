# service/model/lightgbm.py
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from sklearn.model_selection import train_test_split
from sklearn.metrics import (roc_auc_score, accuracy_score, f1_score, classification_report)
from lightgbm import LGBMClassifier, early_stopping, log_evaluation

DEFAULT_PARAMS: Dict[str, Any] = {
    "objective": "binary",
    "boosting_type": "gbdt",
    "n_estimators": 5000,
    "learning_rate": 0.02,
    "num_leaves": 63,
    "max_depth": -1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 0.1,
    "class_weight": "balanced",
    "random_state": 42,
    "n_jobs": -1,
    "verbose": -1,
}

def train_lightgbm(
    X: pd.DataFrame,
    y: pd.Series,
    params: Optional[Dict[str, Any]] = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[LGBMClassifier, Dict[str, Any]]:
    """
    LightGBM 단일 스플릿 학습/평가 러너.
    반환: (학습된 모델, metrics 딕셔너리)
    """
    assert set(y.unique()).issubset({0, 1}), "y는 binary 여야 합니다."
    use_params = dict(DEFAULT_PARAMS)
    if params:
        use_params.update(params)

    # 1) split
    X_tr, X_va, y_tr, y_va = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    # 2) model
    model = LGBMClassifier(**use_params)

    # 3) fit with early stopping
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_tr, y_tr), (X_va, y_va)],
        eval_names=["train", "valid"],
        eval_metric="auc",
        callbacks=[
            early_stopping(stopping_rounds=200, verbose=False),
            log_evaluation(period=100),
        ],
    )

    # 4) metrics
    va_proba = model.predict_proba(X_va)[:, 1]
    va_pred  = (va_proba >= 0.5).astype(int)

    metrics = {
        "auc": float(roc_auc_score(y_va, va_proba)),
        "acc": float(accuracy_score(y_va, va_pred)),
        "f1":  float(f1_score(y_va, va_pred)),
        "report": classification_report(y_va, va_pred, digits=4, output_dict=False),
        "best_iteration_": getattr(model, "best_iteration_", None),
    }
    return model, metrics
