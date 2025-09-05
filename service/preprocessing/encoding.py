import pandas as pd

def do_encoding(df_train: pd.DataFrame, df_test: pd.DataFrame, encoding_cols: list):
    # 원핫인코딩
    df_train = pd.get_dummies(df_train, columns=encoding_cols)
    df_test  = pd.get_dummies(df_test, columns=encoding_cols)

    # train/test의 컬럼을 동일하게 맞춤
    df_train, df_test = df_train.align(df_test, join="outer", axis=1, fill_value=0)

    return df_train, df_test