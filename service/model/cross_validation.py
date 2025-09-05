from sklearn.model_selection import StratifiedKFold
from .metrcis import Metrics_Type

def creat_cv(n_split:int=10, shuffle:bool=True, random_state=42): # cv 만드는 함수
    return StratifiedKFold(n_splits=n_split, shuffle=shuffle, random_state=random_state)

def do_training_with_cv(model, cv, df_train, df_train_target, metrics_type:Metrics_Type) -> float:
    # cross_validation 결과값 주는 함수
    score = 0.0 # socre의 초기값 정의

    for i, (train_index, valid_index) in enumerate(cv.split(df_train, df_train_target)):
        # 위 for문은 StratifiedKFold가 df_train과 df_train_target을
        # 학습용/검증용 인덱스로 나눈 것을 순서대로 꺼내오는 반복문임.
        #################################
        # for문 작성
        #################################
        # 학습용 데이터 -> features, targets로 나눠
        tr_features, tr_targets = df_train.iloc[train_index], df_train_target.iloc[train_index]
        # 평가용 데이터 -> features, targets
        te_features, te_targets = df_train.iloc[valid_index], df_train_target.iloc[valid_index]
        # 모델 학습
        model.fit(tr_features, tr_targets)
        # 평가
        predictions = model.predict_proba(te_features)[:, 1]
        score += metrics_type.value[1](te_targets, predictions)

    return score / cv.n_splits