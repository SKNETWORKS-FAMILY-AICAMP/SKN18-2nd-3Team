import numpy as np
import xgboost as xgb
from .metrcis import Metrics_Type
from sklearn.model_selection import StratifiedKFold
from sklearn.base import clone

# # (선택) 지표 함수 타입에 따라 확률/라벨을 넘기는 보조함수
# def _compute_metric(metric_fn, y_true, proba, threshold=0.5):
#     name = getattr(metric_fn, "__name__", "").lower()
#     # 확률을 기대하는 지표
#     if any(k in name for k in ["auc", "log_loss", "average_precision"]):
#         return float(metric_fn(y_true, proba))
#     # 이외엔 라벨을 기대한다고 가정
#     pred = (proba >= threshold).astype(int)
#     return float(metric_fn(y_true, pred))

def creat_cv(n_split:int=10, shuffle:bool=True, random_state=42): # cv 만드는 함수
    return StratifiedKFold(n_splits=n_split, shuffle=shuffle, random_state=random_state)

# def do_training_with_cv(model, cv, df_train, df_train_target, metrics_type:Metrics_Type) -> float:
#     # cross_validation 결과값 주는 함수
#     score = 0.0 # socre의 초기값 정의

#     for i, (train_index, valid_index) in enumerate(cv.split(df_train, df_train_target)):
#         # 위 for문은 StratifiedKFold가 df_train과 df_train_target을
#         # 학습용/검증용 인덱스로 나눈 것을 순서대로 꺼내오는 반복문임.
#         #################################
#         # for문 작성
#         #################################
#         # 학습용 데이터 -> features, targets로 나눠
#         tr_features, tr_targets = df_train.iloc[train_index], df_train_target.iloc[train_index]
#         # 평가용 데이터 -> features, targets
#         te_features, te_targets = df_train.iloc[valid_index], df_train_target.iloc[valid_index]
#         # 모델 학습
#         model.fit(tr_features, tr_targets)
#         # 평가
#         predictions = model.predict_proba(te_features)[:, 1]
#         score += metrics_type.value[1](te_targets, predictions)

#     return score / cv.n_splits


def do_training_with_cv(model, cv, X, y, metric_fn):
    """
    - model : LGBMClassifier 또는 XGBClassifier 등 sklearn API 모델
    - cv    : StratifiedKFold 등
    - X, y  : pandas DataFrame/Series 권장
    - metric_fn : roc_auc_score, f1_score 등 (확률 or 라벨 필요시 _compute_metric로 처리)
    """
    import lightgbm as lgb
    import xgboost as xgb

    scores = []
    # for tr_idx, va_idx in cv.split(X, y):
    #     X_tr, X_va = X.iloc[tr_idx], X.iloc[va_idx]
    #     y_tr, y_va = y.iloc[tr_idx], y.iloc[va_idx]

    #     # 모델 타입에 따라 분기
    #     if model.__class__.__name__ == "XGBClassifier":
    #         # 불균형 처리
    #         neg, pos = int((y_tr==0).sum()), int((y_tr==1).sum())
    #         spw = neg / max(pos, 1)

    #         # DMatrix로 변환
    #         dtrain = xgb.DMatrix(X_tr, label=y_tr)
    #         dvalid = xgb.DMatrix(X_va, label=y_va)

    #         # booster API 파라미터(필요 시 args에서 가져와도 됨)
    #         params = {
    #             "objective": "binary:logistic",
    #             "eval_metric": "auc",
    #             "eta": getattr(model, "learning_rate", 0.03),
    #             "max_depth": getattr(model, "max_depth", 6),
    #             "subsample": getattr(model, "subsample", 0.8),
    #             "colsample_bytree": getattr(model, "colsample_bytree", 0.8),
    #             "lambda": 0.5,
    #             "alpha": 0.1,
    #             "scale_pos_weight": spw,
    #             "tree_method": getattr(model, "tree_method", "hist"),
    #         }

    #         booster = xgb.train(
    #             params=params,
    #             dtrain=dtrain,
    #             num_boost_round=4000,
    #             evals=[(dvalid, "valid")],
    #             early_stopping_rounds=200,
    #             verbose_eval=False,
    #         )

    #         # 검증 점수 계산
    #         proba = booster.predict(dvalid)
    #         score = metric_fn(y_va, proba)

    #     else:
    #         # LightGBM 등 scikit-learn 호환 모델은 .fit 사용
    #         model.fit(
    #             X_tr, y_tr,
    #             eval_set=[(X_va, y_va)],
    #             eval_metric="auc",
    #             verbose=False
    #         )
    #         proba = model.predict_proba(X_va)[:, 1]
    #         score = metric_fn(y_va, proba)

    #     scores.append(score)

    # return float(np.mean(scores))

    for tr_idx, va_idx in cv.split(X, y):
        X_tr, X_va = X.iloc[tr_idx], X.iloc[va_idx]
        y_tr, y_va = y.iloc[tr_idx], y.iloc[va_idx]

        # 모델 새로 복제(폴드 간 상태 공유 방지)
        mdl = clone(model)

        # ===== LightGBM 분기 =====
        if mdl.__class__.__name__ == "LGBMClassifier":
            mdl.set_params(
                objective="binary",
                boosting_type="gbdt",
                n_estimators=5000, learning_rate=0.02, num_leaves=63,
                subsample=0.8, colsample_bytree=0.8,
                reg_alpha=0.1, reg_lambda=0.1,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1
            )

            mdl.fit(
                X_tr, y_tr,
                eval_set=[(X_tr, y_tr), (X_va, y_va)],
                eval_names=["train", "valid"],
                eval_metric="auc",
                callbacks=[
                    lgb.early_stopping(stopping_rounds=200, verbose=False),
                    lgb.log_evaluation(period=100)
                ]
            )
            proba = mdl.predict_proba(X_va)[:, 1]

        # ===== XGBoost (sklearn 래퍼) 분기 =====
        elif mdl.__class__.__name__ == "XGBClassifier":
            try:
                mdl.set_params(
                    eval_metric="auc",
                    tree_method=mdl.get_xgb_params().get("tree_method", "hist")
                )
                mdl.fit(
                    X_tr, y_tr,
                    eval_set=[(X_va, y_va)],
                    early_stopping_rounds=200,
                    verbose=False,
                )
            except TypeError:
                try:
                    from xgboost.callback import EarlyStopping
                    mdl.fit(
                        X_tr, y_tr,
                        eval_set=[(X_va, y_va)],
                        callbacks=[EarlyStopping(rounds=200, save_best=True)],
                        verbose=False,
                    )
                except Exception:
                    mdl.fit(X_tr, y_tr)  # 최후의 fallback
            proba = mdl.predict_proba(X_va)[:, 1]

        # ===== 기타 sklearn 분기 =====
        else:
            # 표준 API: fit -> predict_proba (없으면 decision_function로 대체)
            mdl.fit(X_tr, y_tr)
            if hasattr(mdl, "predict_proba"):
                proba = mdl.predict_proba(X_va)[:, 1]
            elif hasattr(mdl, "decision_function"):
                # decision_function을 0-1 확률처럼 쓰기 위해 min-max 스케일
                raw = mdl.decision_function(X_va)
                rmin, rmax = raw.min(), raw.max()
                proba = (raw - rmin) / (rmax - rmin + 1e-12)
            else:
                # 확률이 전혀 없으면 예측 라벨만: 지표에 따라 점수 낮을 수 있음
                pred = mdl.predict(X_va)
                proba = pred.astype(float)

        score = _compute_metric(metric_fn, y_va, proba, threshold=0.5)
        scores.append(score)

    return float(np.mean(scores))