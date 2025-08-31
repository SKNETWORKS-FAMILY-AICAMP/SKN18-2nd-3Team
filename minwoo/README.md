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