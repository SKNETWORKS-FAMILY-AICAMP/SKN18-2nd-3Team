import pandas as pd

# 데이터셋을 불러오는 함수
def load_dataset(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

# 데이터셋을 target과 feature로 쪼개자
def split_features_targets(df:pd.DataFrame):
    df_targets = df[]
    df_train = df[]