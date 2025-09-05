import enum #열거형(enumeration)은 고유한 상숫값에 연결된 기호 이름(멤버)의 집합
from sklearn.metrics import roc_auc_score, f1_score

class Metrics_Type(enum.Enum):
    roc_auc_score = (enum.auto(), roc_auc_score)
    f1_score = (enum.auto(), f1_score)