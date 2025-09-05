
import enum
from typing import Union, Dict, Any
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

# class Model_Type(enum.Enum): # enum 클래스 정의
#   # -> XGBosst, LightGBM, 등등 모델 여기에 정의
#   lightgbm = (enum.auto(), LGBMClassifier) # lightgbm 모듈 정의
#   xgboost  = (enum.auto(), XGBClassifier)

# def create_model(model_name:Model_Type, hp:dict): 
#   if model_name not in Model_Type.__members__: # Model_Type에 없으면
#     raise Exception(f"우리 서비스가 제공하지 않는 모델을 입력하셨습니다. >> {model_name}")
#     #__members__는 파이썬에서 enum 클래스 안에 정의된 모든 멤버들을 딕셔너리 형태로 보여주는 속성

#   """
#   모델 인스턴스를 생성해 반환한다.
#   - model_name: 'lightgbm' / 'xgboost' 또는 Model_Type.lightgbm / Model_Type.xgboost
#   - hp: 하이퍼파라미터 dict (기본값은 setdefault로 채움)
#   """
#   cls = model_name.value[1]
#   params: Dict[str, Any] = dict(hp) if hp else {}
  
#   # business_code
#   # model = Model_Type[model_name].value[1](**hp, verbpse=-1)
#   # verbose=-1 로그 안나오게 하는 코드(이상한 경고창 같은거 안나오게 해줌)
#   params.setdefault("random_state", 42)

#   if model_name is Model_Type.lightgbm:
#       # LightGBM 권장 기본값
#       params.setdefault("verbose", -1)   # 로깅 억제
#       # (선택) 자주 쓰는 합리적 디폴트
#       # params.setdefault("n_estimators", 2000)
#       # params.setdefault("learning_rate", 0.05)
#       # params.setdefault("class_weight", "balanced")  
#   elif model_name is Model_Type.xgboost:
#       # XGBoost 권장 기본값
#       params.setdefault("verbosity", 0)   # 로깅 억제
#       params.setdefault("eval_metric", "auc")
#       params.setdefault("tree_method", "hist")  # GPU면 'gpu_hist'로 교체
#       # (선택) 자주 쓰는 합리적 디폴트
#       # params.setdefault("n_estimators", 2000)
#       # params.setdefault("learning_rate", 0.05)  return cls(**params)
#   return cls(**params)
