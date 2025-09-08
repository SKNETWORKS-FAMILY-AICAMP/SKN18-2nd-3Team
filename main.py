import warnings #파이썬 실행 중에 나오는 경고 메세지를 다루는 모듈
warnings.filterwarnings('ignore') #모든 종류의 경고메세지에 대해서 화면에 표시하지 말라는 뜻

import logging #파이썬 내장모듈/ 프로그램 실행 중에 로그 메세지를 출력하거나 파일에 저장할 수 있음
logging.basicConfig(level=logging.INFO) #info이상 레벨만 보이게 해줌

import argparse

import lightgbm as lgb # lightgbm 실행시 로그 자꾸 뜨는거 막는 패키지
#######################
# 코드 정의 영역
#######################
from service.data_setup import do_load_dataset
from service.preprocessing.data_preprocessing import do_preprocessing
from service.model.training import do_training
from service.submission import create_submission_file
from service.submission import clean_column_names
from service.preprocessing.create_feature import rel_major, size_type_last

# LightGBM 실행시 귀찮은 로그 차단
class _SilentLGBMLogger:
    def info(self, msg):    # 일반 로그
        pass
    def warning(self, msg): # 경고 로그
        pass

lgb.register_logger(_SilentLGBMLogger())

def main(args):
    # 1. 데이터를 불러오자
    df_train, df_test, df_train_target =do_load_dataset(
        train_path=args.path_train, test_path=args.path_test, target_name=args.target_name
    )

    # 2. 학습에 도움이 되는 feature 불러오기
    df_train, df_test = size_type_last(df_train, df_test)
    df_train, df_test = rel_major(df_train, df_test)

    # job_size_type_group → 라벨 문자열 컬럼 (모델 입력에 불필요)
    if "job_size_type_group" in df_train.columns:
        df_train.drop(columns=["job_size_type_group"], inplace=True)
    if "job_size_type_group" in df_test.columns:
        df_test.drop(columns=["job_size_type_group"], inplace=True)

    # (옵션) 숫자형 보정
    for c in ["job_size_type_code", "rel_major_code"]:
        if c in df_train.columns:
            df_train[c] = df_train[c].astype("int32")
        if c in df_test.columns:
            df_test[c] = df_test[c].astype("int32")

    # 3. 데이터를 전처리하자
    df_train, df_test = do_preprocessing(
        df_train=df_train, #trian 데이터를 받곘다
        df_test=df_test, #test 데이터를 받겠다
        drop_cols=args.drop_cols,
        encoding_cols=args.encoding_cols,
        transform_cols=args.transform_cols
    )

    # 4. xgboost 오류 방지(컬럼에 기호가 들어가지 않게 막아주는 부분)
    df_train, df_test = clean_column_names(df_train, df_test)

    # 5. 모델을 학습시키자
    is_model = do_training(df_train, df_train_target, args)
    logging.info(f"학습에 사용한 모델: {args.model_name}")

    # 6. submission 결과 제출
    create_submission_file(is_model=is_model, df_test=df_test)

if __name__ == "__main__":
    ################################
    # 코드 실행 영역
    ################################
    args = argparse.ArgumentParser() # argparseArgumentParser() -> 기능을 쓸 수 있는 객체를 만들어줌.
    # .add_argument() → 받을 옵션/인자들을 등록.
    args.add_argument("--path_train", default="./Data/aug_train.csv", type=str)
    args.add_argument("--path_test", default="./Data/aug_test.csv", type=str)
    args.add_argument("--path_submission", default="./Data/sampl_submission.csv", type=str)
    args.add_argument("--target_name", default="target", type=str)
    
    # EDA 분석결과 집어넣기
    args.add_argument("--drop_cols", default=['enrollee_id','city','city_development_index','gender'], type=str)
    args.add_argument("--transform_cols", default=[], type=str)
    args.add_argument("--encoding_cols", default=[
        'relevent_experience',
        'enrolled_university',
        'education_level',
        'major_discipline',
        'experience',
        'company_size',
        'company_type',
        'last_new_job'
        ])
    args.add_argument("--model_name", default="decisiontree") # 학습할 모델 선택하는 부분
    args.add_argument("--hp", default={}, type=dict)
    args.add_argument("--decisiontree.max_depth", default="10")
    args.add_argument("--decisiontree.min_samples_leaf", default="5")
    args.add_argument("--decisiontree_max_depth", default=10, type=int) # 디시젼트리 하이퍼파리미터 설정하는 부분
    args.add_argument("--decisiontree_min_samples_leaf", default=5, type=int) # 디시젼트리 하이퍼파라미터 설정하는 부분 

    main(args.parse_args()) # 터미널에서 입력된 값을 실제로 해석해서 args 안에 저장.