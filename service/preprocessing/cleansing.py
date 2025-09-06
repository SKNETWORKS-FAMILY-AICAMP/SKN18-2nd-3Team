#데이터 클렌징
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype # 특정 컬럼이 숫자형인지 판단

def __fillna(df_train:pd.DataFrame, df_test:pd.DataFrame):
    # 결측치 파악
    train_none_cols = df_train.isnull().sum()[df_train.isnull().sum() > 0].index
    test_none_cols = df_test.isnull().sum()[df_test.isnull().sum() > 0].index
    none_cols = list(set(train_none_cols) | set(test_none_cols)) # -> 결측치들의 합집합
    # 결측치들 리스트에 담았음.

    for col in none_cols: # 결측치 처리하는 부분
        # train데이터 결측치처리
        if is_numeric_dtype(df_train[col]): # 수치형 데이터 결측치 처리
            _value = df_train[col].mean()
        else:
            _value = df_train[col].mode()[0] # 범주형 데이터 결측치 처리

        # test/train 결측치 채우기
        df_train[col].fillna(_value, inplace = True) #train에 결측치 처리
        if col in df_test.columns: #df_train 컬럼에 있는게 test에도 있으면 결측치를 채움(범주형)
            df_test[col].fillna(_value, inplace=True)
    
    return df_train, df_test

def __drop_cols(df_train:pd.DataFrame,df_test:pd.DataFrame, drop_cols:list): #컬럼 드랍함수
    return df_train.drop(drop_cols, axis=1), df_test.drop(drop_cols, axis=1)

def __tramsform_cols(df_train:pd.DataFrame, df_test:pd.DataFrame, transform_cols:list): #왜도/첨도 처리함수
    for col in transform_cols:
        df_train[col] = df_train[col].map(lambda x:np.log1p(x))
        df_test[col] = df_test[col].map(lambda x:np.log1p(x))

    return df_train, df_test

def do_cleansing(df_train:pd.DataFrame, df_test:pd.DataFrame, drop_cols:list, transform_cols:list):
    # 1. row 중복 데이터 제거
    df_train = df_train.drop_duplicates()

    # 2. 결측치를 치환(통계값 <- train데이터에서 와야함. test데이터에서 오면 안됨!)
    df_train, df_test = __fillna(df_train, df_test)

    # 3. 필요없는 컬럼 제거
    df_train, df_test = __drop_cols(df_train, df_test, drop_cols=drop_cols)

    # 4. 왜도/첨도 처리
    df_train, df_test = __tramsform_cols(df_train, df_test, transform_cols=transform_cols)

    # 5. 검증
    assert df_train.shape[1] == df_test.shape[1], "train과 test의 컬럼 수가 일치하지 않습니다."
    
    return df_train, df_test