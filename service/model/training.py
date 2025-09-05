# 트레이닝 시키는 파일
from .models import create_model
from .cross_validation import creat_cv, do_training_with_cv
from .metrcis import Metrics_Type
import logging

def do_training(df_train, df_train_target, args):
    result = None # 결과 제출 유무는 result 값으로 파악할 수 있다.
    model = create_model(model_name=args.model_name, hp=args) #hp -> 하이퍼파라미터
    score_by_cv_roc_auc_score = do_training_with_cv(
        model, creat_cv(), df_train, df_train_target, Metrics_Type.roc_auc_score
    )
    score_by_cv_f1_score = do_training_with_cv(
        model, creat_cv(), df_train, df_train_target, Metrics_Type.f1_score
    )
    logging.info(f"score_by_cv_roc_auc_score:{score_by_cv_roc_auc_score}")
    logging.info(f"score_by_cv_f1_score:{score_by_cv_f1_score}")

    best_score_result = max(score_by_cv_f1_score, score_by_cv_roc_auc_score)
    # f1_score와 roc_auc_score 중에 더 큰 값 선택

    if best_score_result >= 0.7: # 선택된 값이 0.7 이상이면
        result = model # result에 결과값 입력
    
    return result # 리턴값으로 result 받음