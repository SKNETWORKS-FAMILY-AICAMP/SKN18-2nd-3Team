# 데이터 학습에 도움이 되는 feature 생성
import pandas as pd
import numpy as np
from service.preprocessing.encoding import do_encoding #인코딩함수 불러오기
from service.preprocessing.cleansing import do_cleansing #클렌징함수 불러오기
from sklearn.impute import SimpleImputer

'''
만들 Feautre 리스트
1. relevent_experience + major_discipline : rel_major_code
2. company_size + company_type + last_new_job : job_size_type_code3.
3. exp_bin_code: 경험 구간화 결과 (정수 코드, -1은 NaN)
4. rel_exp_score: 경력×관련경험 (float)
5. stem_related: STEM×관련경험 (0/1)

6. training_per_year
-> training_hours / (experience_num+1)

7.training_rel / training_no_rel
-> training_rel = training_hours × rel_exp_flag
-> training_no_rel = training_hours × (1 - rel_exp_flag)

8. training_stem / training_nonstem
-> training_stem = training_hours × stem_flag
-> training_nonstem = training_hours × (1 - stem_flag)

9. training_expbin* 일괄 생성 (수치형)
-> exp_bin을 원핫 더미로 만들고 각 더미 × training_hours
-> 예: training_exp_bin_exp_0_2 = (경력 0–2 구간 여부) × 교육시간 
'''

def size_type_last(df_train:pd.DataFrame, df_test:pd.DataFrame):
    
    # 공통 설정
    other_cols = ['company_size','company_type']
    group2code = {
        "No Response": 0,
        "New Graduate": 1,
        "Experienced Unemployed": 2,
        "Other_NoResponse": 3,
        "Other_NewGraduate": 4,
        "Other_Experienced": 5,
        "Complete": 6
    }

    def _classify(row):
        cs_nan = pd.isna(row['company_size'])
        ct_nan = pd.isna(row['company_type'])
        lnj    = row['last_new_job']

        if cs_nan and ct_nan:  # both NaN
            if pd.isna(lnj):
                return "No Response"            # both nan + last_new_job NaN
            elif lnj == "never":
                return "New Graduate"           # both nan + never
            else:
                return "Experienced Unemployed" # both nan + 숫자/기타

        else:
            return "Complete"
    def process_df(df):
        # 1) 마스크 (df마다 따로 계산)
        both_nan_mask    = df['company_size'].isna() & df['company_type'].isna()
        one_nan_mask     = df['company_size'].isna() ^ df['company_type'].isna()

        # 2) one_nan 서브셋만 최빈값 대치
        imputer = SimpleImputer(strategy='most_frequent')
        sub = df.loc[one_nan_mask, other_cols].copy()
        if len(sub) > 0:
            sub_imputed = pd.DataFrame(
                imputer.fit_transform(sub),
                index=sub.index,
                columns=other_cols
            )
            df.loc[one_nan_mask, 'company_size'] = sub_imputed['company_size'].values
            df.loc[one_nan_mask, 'company_type'] = sub_imputed['company_type'].values

        # 3) 그룹 라벨 + 코드
        df['job_size_type_group'] = df.apply(_classify, axis=1)
        df['job_size_type_code']  = df['job_size_type_group'].map(group2code).astype(int)
        return df

    # === train / test 모두 처리 ===
    df_train = process_df(df_train)
    df_test  = process_df(df_test)


def rel_major(df_train:pd.DataFrame, df_test:pd.DataFrame):
    def pick_major_col(df):
        for c in ['major_discipline', 'major_dicipline']:
            if c in df.columns:
                return c
        raise AssertionError("major_discipline(또는 major_dicipline) 컬럼이 필요합니다.")

    major_col_tr = pick_major_col(df_train)
    major_col_te = pick_major_col(df_test)

    # 1) 텍스트 표준화 (원본은 변경하지 않음)
    def norm_rel(x):
        if pd.isna(x):
            return np.nan
        s = str(x).strip()
        sl = s.lower()
        if sl.startswith('has'): return 'Has'
        if sl.startswith('no'):  return 'No'
        return s

    def build_cross_text(df, major_col):
        rel_txt   = df['relevent_experience'].apply(norm_rel)
        major_txt = df[major_col].astype('string')  # 결측은 <NA> 유지
        # 파생 텍스트에서만 결측을 'NA'로 표기 (원본 df는 그대로)
        return rel_txt.astype('string').str.cat(major_txt, sep='|', na_rep='NA')
    
    # 2) 교차변수 생성 (train에 fit → test에 transform)
    cross_train_txt = build_cross_text(df_train, major_col_tr)

    # train: 카테고리 고정 후 코드 부여
    cross_train_cat = cross_train_txt.astype('category')
    train_categories = list(cross_train_cat.cat.categories)  # 고정 카테고리
    df_train['rel_major_code'] = cross_train_cat.cat.codes.astype('int32')  # 결측/미지 조합은 -1

    # test: 동일 카테고리 세트로 매핑 (미지 조합은 -1)
    cross_test_txt = build_cross_text(df_test, major_col_te)
    txt2code = {cat: i for i, cat in enumerate(train_categories)}
    df_test['rel_major_code'] = cross_test_txt.map(txt2code).fillna(-1).astype('int32')