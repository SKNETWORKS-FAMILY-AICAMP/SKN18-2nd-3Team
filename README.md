# SKN18-2nd-3Team

# 📑 새로 만든 피처 설명

## A) 기반 전처리/플래그

- **experience_num**  
  - 원본 `experience` 문자열을 숫자로 변환  
  - 규칙: `"<1" → 0`, `"1"~"20" → 해당 숫자`, `">20" → 21`, 그 외/결측 → `NaN`  
  - 목적: 경력을 **연속형/순서형**으로 모델에 쓰기 쉽게 표준화  

- **rel_exp_flag**  
  - `relevent_experience == "Has relevent experience"`이면 `1`, 아니면 `0`  
  - 목적: **관련 경력 유무**를 이진값으로 명확하게 반영  

- **stem_flag**  
  - `major_discipline == "STEM"`이면 `1`, 아니면 `0`  
  - 목적: **STEM 전공 여부**를 이진값으로 반영  

---

## B) 경력 구간 & 전공×관련경험 그룹

- **exp_bin** *(범주형)*  
  - `experience_num`를 5구간으로 비닝  
  - 구간: `0–2 (exp_0_2)`, `3–5`, `6–9`, `10–14`, `15+`  
  - 목적: **비선형/구간별 효과**를 쉽게 포착  

- **major_relexp_grp** *(범주형)*  
  - 전공(STEM/NonSTEM) × 관련경험(Rel/NoRel) 조합  
  - 값 예시: `STEM_Rel`, `STEM_NoRel`, `NonSTEM_Rel`, `NonSTEM_NoRel`, 결측 포함 시 `UNK`  
  - 목적: **전공과 관련경험의 결합 효과**를 직접적인 그룹으로 표현  

---

## C) 핵심 상호작용 (경력·전공·관련경험)

- **rel_exp_score**  
  - `experience_num × rel_exp_flag`  
  - 의미: 관련경력이 있는 경우에만 경력의 양을 반영하는 점수  
  - 의도: “관련 경력”의 강도를 수치로 표현  

- **stem_related**  
  - `stem_flag × rel_exp_flag`  
  - 의미: STEM 전공 + 관련경험을 동시에 만족할 때 `1`, 아니면 `0`  
  - 의도: **기술 직무 적합도 높은 조합**을 별도로 표시  

---

## D) training_hours 조합 (있을 때만 생성)

- **training_per_year**  
  - `training_hours / (experience_num+1)`  
  - 의미: **경력 1년당 교육 시간** (경력이 적을수록 같은 시간의 교육이 더 큰 의미)  
  - 의도: 교육의 **상대적 강도**를 경력 규모로 정규화  

- **training_rel / training_no_rel**  
  - `training_rel = training_hours × rel_exp_flag`  
  - `training_no_rel = training_hours × (1 - rel_exp_flag)`  
  - 의미: 관련경력이 있는 사람/없는 사람에게서의 교육시간 효과를 분리  
  - 의도: 교육 효과가 **관련경험 유무에 따라 다를 수 있음**을 모델이 포착  

- **training_stem / training_nonstem**  
  - `training_stem = training_hours × stem_flag`  
  - `training_nonstem = training_hours × (1 - stem_flag)`  
  - 의미: STEM/비-STEM 집단별 교육시간 효과 분리  
  - 의도: 전공에 따른 **교육 효용 차이**를 반영  

- **training_exp_bin_*** *(수치형)*  
  - `exp_bin`을 원핫 더미로 만들고 각 더미 × `training_hours`  
  - 예: `training_exp_bin_exp_0_2 = (경력 0–2 구간 여부) × 교육시간`  
  - 의미: **경력 구간별 교육시간의 상호작용 효과**  
  - 의도: “경력 초기/중기/고경력”에 따라 교육의 **민감도 차이**를 모델이 학습  
