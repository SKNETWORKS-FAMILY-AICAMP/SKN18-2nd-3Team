import pandas as pd
from .cleansing import do_cleansing
from .encoding import do_encoding
# from .create_feature import size_type_last, rel_major


def do_preprocessing(df_train: pd.DataFrame, df_test: pd.DataFrame, drop_cols:list, #  모델 학습 전 데이터 전처리 함수
                    transform_cols: list, encoding_cols:list):

    # 1. cleansing
    df_train, df_test = do_cleansing(df_train, df_test, drop_cols, transform_cols)

    # 2. 학습을 위해 생성한 feature와 기존 feature들에 대해서 결합
    # df_train, df_test = size_type_last(df_train, df_test)
    # df_train, df_test = rel_major(df_train, df_test)

    # 3. change datatype for encoding
    df_train, df_test = do_encoding(df_train, df_test, encoding_cols)

    return df_train, df_test