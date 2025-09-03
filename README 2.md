# 만들고자 하는 것 : HR Analytics: Job Change of Data Scientists의 Feature 분석
---
# 필요한 기능들 
1. HR Analytics: Job Change of Data Scientists 데이터셋 로드 
2. 데이터전처리 
  - 데이터셋을 분석(EDA)
  - 데이터셋 클린징(결측치, 중복데이터, 왜도/첨도)
  - 학습에 도움이되는 feature 생성 
  - 범주형 데이터를 숫자형 데이터로 변환 
  - 숫자 데이터의 범위를 통일(scaling)
  - (옵션) unbalance dataset인 경우, 처리 필요
3. 모델링 
  - 모델 생성
  - 하이퍼 파라미터 튜닝 
  - cross validation 진행 
4. 평가 
  - underfitting / overfitting 
  - matrix(평가지표)를 이용해서 점수 확인 
  ---

  # 설계를 하자!!!!!!!!!!!!! 제발!!!!!!!!!!!!!
- ## 어떤 폴더들이 필요하니? 
  - 1. model 폴더: 여기에 각종 모델들을 만들고 관리해야겠다.
  - 2. service 폴더: 프로젝트가 구동되기 위한 필요한 파일들을 저장
    - 2-1. preprocessing: 전처리와 관련한 파일들을 저장하자
  - 3. minwoo 폴더: 가장 상위에 있는 폴더, main파일은 여기에 저장
- ## 이제 어떤 파일들이 필요할까?
  - 1. minwoo
    - main.py: 메인파일로 여기서 프로젝트 실행
    - data_setup.py: 데이터셋 받은걸 여기서 1차적으로 처리해주기
    - eda.ipynb : 주피터 노트북으로 eda 확인하면서 진행하자
  - 2. model
    - lightgbm.py: 라이트gbm 모델 만드는 파일
  - 3. service
    - cleansing.py
  - 4. preprocessing