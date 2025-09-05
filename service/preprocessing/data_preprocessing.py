import pandas as pd
from .cleansing import do_cleansing
from .encoding import do_encoding

def do_preprocessing(df_train: pd.DataFrame, df_test: pd.DataFrame, drop_cols:list, #  모델 학습 전 데이터 전처리 함수
                    transform_cols: list, encoding_cols:list):

    # 1. cleansing
    df_train, df_test = do_cleansing(df_train, df_test, drop_cols, transform_cols)

    # 2. change datatype for encoding
    df_train, df_test = do_encoding(df_train, df_test, encoding_cols)

    return df_train, df_test