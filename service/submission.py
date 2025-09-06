import re
from service.data_setup import load_dataset

def clean_column_names(df_train, df_test): #xgboost 사용 간 컬럼 이름에 기호 들어가는거 방지
    df_train.columns = [re.sub(r'[\[\]<>]', '_', str(c)) for c in df_train.columns]
    df_test.columns  = [re.sub(r'[\[\]<>]', '_', str(c)) for c in df_test.columns]
    return df_train, df_test

def create_submission_file(is_model, df_test):
    if not is_model:
        return # 정의되지 않은 모델이면 함수 종료 시켜버림
    
    predictions = is_model.predict_proba(df_test)[:,1]
    df_submission = load_dataset("./Data/sample_submission.csv")
    df_submission['target'] = predictions
    df_submission.to_csv("./result_csv/result_submission.csv", header=True, index=False)