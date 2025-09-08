#lightgbm_model 제작
import enum
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.tree import DecisionTreeClassifier # 디시젼트리 모델
import inspect #  파이썬 객체(함수, 클래스, 메서드 등)의 내부 정보를 실행 중에 확인할 수 있게 해줌

class Model_Type(enum.Enum):# enum 클래스 정의
    # -> XGBosst, LightGBM, 등등 모델 여기에 정의
    lightgbm = (enum.auto(), LGBMClassifier) # lightgbm 모듈 정의
    xgboost = (enum.auto(), XGBClassifier) # xgboost 모듈 정의
    decisiontree = (enum.auto(), DecisionTreeClassifier)

def create_model(model_name:Model_Type, hp:dict): # lightgbm 모델 제작 함수
    if model_name not in Model_Type.__members__: # Model_Type에 없으면
        raise Exception(f"우리 서비스가 제공하지 않는 모델을 입력하셨습니다. >> {model_name}")
    #__members__는 파이썬에서 enum 클래스 안에 정의된 모든 멤버들을 딕셔너리 형태로 보여주는 속성

    # business_code
    model_class = Model_Type[model_name].value[1](**hp, verbose=-1)
    #verbose=-1 로그 안나오게 하는 코드(이상한 경고창 같은거 안나오게 해줌)

    #  DecisionTree만 따로 처리
    if model_name == "decisiontree":
        model = model_class(
            max_depth=hp.decisiontree_max_depth, # 하이퍼파라미터 받을 수 있게 세팅
            min_samples_leaf=hp.decisiontree_min_samples_leaf # 하이퍼파라미터 받을 수 있게 세팅
        )
        model = model(**hp.__dict__)
    else:
        model = model(**hp.__dict__, verbose=-1)

    return model

class Model_Type(enum.Enum):
    lightgbm = (enum.auto(), LGBMClassifier)
    xgboost = (enum.auto(), XGBClassifier)
    decisiontree = (enum.auto(), DecisionTreeClassifier)

def create_model(model_name: str, hp):
    if not isinstance(hp, dict):
        hp = vars(hp)

    # 1) 모델 이름 판별
    if model_name not in Model_Type.__members__:
        raise ValueError(f"우리 서비스가 제공하지 않는 모델입니다. >> {model_name}")

    # 2) model_class 호출
    model_cls = Model_Type[model_name].value[1]

    # 3) 해당 모델이 실제로 받는 파라미터만 전달
    sig = inspect.signature(model_cls.__init__)
    allowed = {k: v for k, v in hp.items() if k in sig.parameters}

    # 4) verbose는 지원하는 모델에만 넣기(ligthgbm이랑 xgboost)
    if 'verbose' in sig.parameters and 'verbose' not in allowed:
        allowed['verbose'] = -1
    if 'verbosity' in sig.parameters and 'verbosity' not in allowed:
        allowed['verbosity'] = -1

    # 5) 최종 생성
    model = model_cls(**allowed)
    return model