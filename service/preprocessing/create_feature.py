# 데이터 학습에 도움이 되는 feature 생성
import pandas as pd
import numpy as np

'''
만들 Feautre 리스트
relevent_experience + major_discipline : rel_major_code
company_size + company_type + last_new_job : job_size_type_code3.
exp_bin_code: 경험 구간화 결과 (정수 코드, -1은 NaN)
rel_exp_score: 경력×관련경험 (float)
stem_related: STEM×관련경험 (0/1)

training_per_year
training_hours / (experience_num+1)

training_rel / training_no_rel
training_rel = training_hours × rel_exp_flag
training_no_rel = training_hours × (1 - rel_exp_flag)

training_stem / training_nonstem
training_stem = training_hours × stem_flag
training_nonstem = training_hours × (1 - stem_flag)

training_expbin* 일괄 생성 (수치형)
exp_bin을 원핫 더미로 만들고 각 더미 × training_hours
예: training_exp_bin_exp_0_2 = (경력 0–2 구간 여부) × 교육시간 
'''

def create_feature():
    pass