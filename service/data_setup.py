import pandas as pd

# 데이터셋을 불러오는 함수
def load_dataset(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

# 데이터셋을 target과 feature로 쪼개자
def split_features_targets(df:pd.DataFrame, target_name:str) -> tuple:
    # 변수가 2개니까 튜플로 반환하는거다.
    df_targets = df[target_name]
    df_feature= df.drop([target_name], axis=1)
    return df_feature, df_targets

def do_load_dataset(train_path:str, test_path:str, target_name:str):
    df_train_full = load_dataset(path=train_path)
    df_test = load_dataset(path=test_path)

    df_train, df_trian_target = split_features_targets(
        df=df_train_full, target_name=target_name
    )

    return df_train, df_test, df_trian_target