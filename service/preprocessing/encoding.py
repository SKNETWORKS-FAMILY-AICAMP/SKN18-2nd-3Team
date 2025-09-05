import pandas as pd
from service.data_setup import do_load_dataset
from sklearn.preprocessing import LabelEncoder
from pandas.api.types import CategoricalDtype


# 인코딩 전에 컬럼이 범주형인지 아닌지 구분하는 함수 제작
def predict_categorical(df_train:pd.DataFrame, df_test:pd.DataFrame):
    def get_categorical_cols(df_category):
        return [ # 리스트 컴프리헨션 사용
            col for col in df_category.columns
            if pd.api.types.is_object_dtype(df_category[col]) or isinstance(df_category[col].dtype, CategoricalDtype)
        ]
    return get_categorical_cols(df_train), get_categorical_cols(df_test)

df_train, df_test = do_load_dataset()
category_train, category_test = predict_categorical(df_train, df_test)
city_feature = 'city'


def do_encoding(df_train:pd.DataFrame, df_test:pd.DataFrame):
    # 원핫인코딩 진행부분
    ohe_cols = [col for col in category_train if col != city_feature]
    df_train_ohe = pd.get_dummies(df_train, columns=ohe_cols)
    df_test_ohe = pd.get_dummies(df_test, columns=ohe_cols)

    # 라벨인코딩 진행부분
    le = LabelEncoder()
    for df in [df_train_ohe, df_test_ohe]:
        if city_feature in df.columns:
            df[city_feature + '_le'] = le.fit_transform(df[city_feature].astype(str))
            df.drop(columns=[city_feature], inplace=True)

    # 원핫인코딩 & 라벨인코딩한거 합치는 부분
    df_train_encoding, df_test_encoding = df_train_ohe.align(df_test_ohe, join='outer', axis=1, fill_value=0)

    return  df_train_encoding, df_test_encoding