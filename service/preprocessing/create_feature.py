# 데이터 학습에 도움이 되는 feature 생성
import pandas as pd
import numpy as np
from service.preprocessing.encoding import do_encoding #인코딩함수 불러오기
from service.preprocessing.cleansing import do_cleansing #클렌징함수 불러오기
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

def create_feature():
    pass