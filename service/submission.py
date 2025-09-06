import re
from service.data_setup import load_dataset

# service/submission.py
import pandas as pd

def _align_X_to_model_columns(model, X: pd.DataFrame) -> pd.DataFrame:
    # 1) scikit-learn 스타일 (최근 xgboost, lightgbm도 지원)
    cols = getattr(model, "feature_names_in_", None)
    if cols is None:
        # 2) XGBoost booster
        try:
            cols = model.get_booster().feature_names
        except Exception:
            cols = None
    if cols is None and hasattr(model, "booster_"):
        # 3) LightGBM booster
        try:
            cols = model.booster_.feature_name()
        except Exception:
            cols = None
    if cols is None:
        raise ValueError("모델의 학습 컬럼 목록을 확인할 수 없습니다.")
    # 학습에 없던 컬럼은 버리고, 부족한 컬럼은 0으로 채움
    return X.reindex(columns=list(cols), fill_value=0)

def create_submission_file(is_model, df_test):
    if is_model is None:
        # 학습 점수 미달 등으로 모델이 없는 경우 처리
        print("모델이 없습니다. (is_model=None)")
        return
    # 🔧 여기서 컬럼 정렬
    df_test_aligned = _align_X_to_model_columns(is_model, df_test)

    # 이진분류일 때
    proba = is_model.predict_proba(df_test_aligned)[:, 1]
    # ... 이하 저장 로직 그대로 ...
