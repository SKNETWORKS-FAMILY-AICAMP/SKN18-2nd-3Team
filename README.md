📌 Main Thema  
**부트캠프에 대한 회사와 지원자의 자가진단 시스템 개발**

---

## 👨‍👩‍👧‍👦 팀 소개  

| 이상효 👩‍💻 | 황민우 👨‍💻 | 채린 👩‍💻 | 김창현 👩‍💻 | 최은정 👩‍💻 |
|------------|------------|------------|------------|------------|
| [@usey10](https://github.com/lsh7159) | [@Lanvizu](https://github.com/Lanvizu) | [@Hyeseo20](https://github.com/Hyeseo20) | [@pbr2858](https://github.com/pbr2858) | [@eunjeong0911](https://github.com/eunjeong0911) |

---

# 1️⃣ 프로젝트 개요  

## 🎯 Motivation  

### 🔹 4차 산업혁명
- **핵심기술: 융합기술**  
  - 독립적이던 기술의 결합 → 혁신적인 서비스 창출  
  - 단일 기술 중심이었던 과거 산업혁명과 차별화  
- **기업**: 빠른 변화 속도를 따라가기 위한 전문 인력 필요  
- **대학 교육 한계** → 실무 중심 교육 모델 필요  
- **부트캠프**:  
  - 3~12개월 단기 집중 교육  
  - 프로그래밍, 데이터 분석, AI/ML 중심  
  - 2010년대 후반부터 전 세계적으로 확산
    <img width="893" height="512" alt="image" src="https://github.com/user-attachments/assets/d4a815ff-2eaf-4787-b7ff-56ec1d89fae5" />

### 🔹 부트캠프 규모 및 추이  
- **글로벌**  
  - 미국: 2013년 약 30개 → 2020년 100개 이상  
  - 수강생: 2013년 약 2,000명 → 2020년 약 40,000명  
- **한국**  
  - 2016년 이후 정부·민간 주도로 급성장  
  - AI·데이터 사이언스, 핀테크, 블록체인 과정 증가  
- **현재**  
  - 데이터 사이언스/AI 과정 비중 확대  
  - 기업 맞춤형 부트캠프 증가
    <img width="903" height="481" alt="image" src="https://github.com/user-attachments/assets/8285226f-c6f7-4b36-9be2-c4aaff77b7df" />



### 🔹 SKN18_2nd_3Team 문제의식  
- 기술 변화 속도 ↑ → 실무형 부트캠프 수요 ↑  
- 기업: **인재육성 관련 데이터 필요**  
- 지원자: **자가진단 시스템 필요**  
- 👉 회사·지원자 관점에서 **자가진단 및 대응책 마련** 프로그램 개발  

---

## Dataset 소개
**HR Analytics: Job Change of Data Scientists**
- **데이터 개요**:  
  - 총 **19,158개 관측치**와 **14개 변수**로 구성된 HR 분석용 데이터셋.  
  - 지원자의 교육, 경력, 회사 관련 정보 등을 포함하며, **교육 후 회사 합류 여부(target))**를 예측하는 이진 분류 문제




---

## 🤖 모델 개발  

- **Dataset**: *HR Analytics Job Change of Data Scientists*  

### 📂 변수 (Feature Selection)  
- **Drop**  
  `enrollee_id`, `city`, `city_development_index`, `gender`  
- **Survived**  
  `relevent_experience`, `enrolled_university`, `education_level`, `major_discipline`,  
  `experience`, `company_size`, `company_type`, `last_new_job`, `training_hours`  
- **Target**  
  `0 = 입사안함`, `1 = 입사`  

### 🛠️ Feature Engineering  
1. `relevent_experience + major_discipline → rel_major_code`  
2. `company_size + company_type + last_new_job → job_size_type_code`  

### 📊 Model  
- **XGBoost**  
- **LightGBM**  

---

## 🖥️ 시스템 구조  

### 📊 Company Info & Candidate Info  
- 화면 상단: **입사 확률 시그널 표시**  
  - 🔴 Red: 20% 미만  
  - 🟡 Yellow: 20% ~ 60%  
  - 🟢 Green: 60% 이상
    <img width="1491" height="187" alt="image" src="https://github.com/user-attachments/assets/5b5467f1-6820-4309-b618-83029523797d" />
  

#### Company View  
1. **취업경력별 입사가능성**  
   - 신입 / 이직준비생 / 현직자 → 그래프화 + Hover 시 데이터 수 표시
     <img width="1469" height="402" alt="image" src="https://github.com/user-attachments/assets/8575e9d2-9007-4e5b-8768-42afd2b2a4db" />

2. **지원자 학력 & 재학 상태**  
   - 학력/재학상태 비율 그래프 + Signal 수치화
     <img width="1467" height="469" alt="image" src="https://github.com/user-attachments/assets/28ee35bd-bbfe-48bb-b2f6-5cd2e3b96b62" />

3. **전공 Level & 연차 분석**  
   - 전공별 Signal 비율 그래프 + 표
     <img width="1466" height="486" alt="image" src="https://github.com/user-attachments/assets/e0d8aec7-857b-43c6-a83e-03d4425be8df" />

   - 연차별 Signal 수치 Line Graph
     <img width="1521" height="519" alt="image" src="https://github.com/user-attachments/assets/a8fad772-15a2-4311-9316-91e31ef5448f" />

4. **모델 Raw Data 시각화**  
   - 변수(Feature)별 Target 매핑  
    <img width="1476" height="476" alt="image" src="https://github.com/user-attachments/assets/c1a4d278-adea-4897-9dfe-0327939a84b8" />

#### Candidate View (자가진단)  
1. **프로필 입력**  
   - 재직 경험 여부 / 총 경력  
   - 전공명 + 관련경력 여부  
   - 학력 + 현재 상태
     <img width="1566" height="764" alt="image" src="https://github.com/user-attachments/assets/e1af72d1-5a06-4175-ae30-c4738b4e7bd3" />

2. **예측 결과 출력**  
   - 교육 후 당사회사 합류 가능성 확률로 표시
   - 합류 가능성 수준을 Signal로 표시
   - FeedBack 제공
   <img width="1600" height="439" alt="image" src="https://github.com/user-attachments/assets/ed432c29-7926-4831-bf03-81e7c0e11686" />

