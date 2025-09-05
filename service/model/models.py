#lightgbm_model 제작
import enum
from lightgbm import LGBMClassifier

class Model_Type(enum.Enum): # enum 클래스 정의
  # -> XGBosst, LightGBM, 등등 모델 여기에 정의
  lightgbm = (enum.auto(), LGBMClassifier) # lightgbm 모듈 정의

def create_model(model_name:Model_Type, hp:dict): # lightgbm 모델 제작 함수
  if model_name not in Model_Type.__members__: # Model_Type에 없으면
    raise Exception(f"우리 서비스가 제공하지 않는 모델을 입력하셨습니다. >> {model_name}")
    #__members__는 파이썬에서 enum 클래스 안에 정의된 모든 멤버들을 딕셔너리 형태로 보여주는 속성

  # business_code
  model = Model_Type[model_name].value[1](**hp, verbpse=-1)
  #verbose=-1 로그 안나오게 하는 코드(이상한 경고창 같은거 안나오게 해줌)

  return model