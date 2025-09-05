# service/model/xgboost.py
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, accuracy_score, f1_score, classification_report
)
from xgboost import XGBClassifier

DEFAULT_PARAMS: Dict[str, Any] = {
    "n_estimators": 4000,         # early_stopping으로 자동 절단
    "learning_rate": 0.03,        # eta
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_lambda": 0.5,            # L2
    "reg_alpha": 0.1,             # L1
    "random_state": 42,
    "tree_method": "hist",        # GPU면 'gpu_hist'로 교체 가능
    "eval_metric": "auc",
    "verbosity": 0,
}

def _with_scale_pos_weight(params: Dict[str, Any], y_tr: pd.Series) -> Dict[str, Any]:
    # 불균형 자동 보정
    neg = int((y_tr == 0).sum())
    pos = int((y_tr == 1).sum())
    spw = neg / max(pos, 1)
    p = dict(params)
    p.setdefault("scale_pos_weight", spw)
    return p

def train_xgboost(
    X: pd.DataFrame,
    y: pd.Series,
    params: Optional[Dict[str, Any]] = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[XGBClassifier, Dict[str, Any]]:
    """
    XGBoost 단일 스플릿 학습/평가 러너 (sklearn API).
    반환: (학습된 모델, metrics 딕셔너리)
    """
    assert set(y.unique()).issubset({0, 1}), "y는 binary 여야 합니다."

    # 1) split
    X_tr, X_va, y_tr, y_va = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    # 2) params (scale_pos_weight 자동 설정)
    use_params = dict(DEFAULT_PARAMS)
    if params:
        use_params.update(params)
    use_params = _with_scale_pos_weight(use_params, y_tr)

    # 3) model
    model = XGBClassifier(**use_params)

    # 4) fit with early stopping (XGBoost 1.6.x에서도 사용 가능)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_tr, y_tr), (X_va, y_va)],
        early_stopping_rounds=200,
        verbose=False,
    )

    # 5) metrics
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
