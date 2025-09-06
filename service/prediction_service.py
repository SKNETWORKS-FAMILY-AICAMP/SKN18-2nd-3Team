import pickle
import pandas as pd
import numpy as np
import os
import logging

# pandas 경고 해결 설정
pd.set_option('future.no_silent_downcasting', True)

# 전처리 모듈들 import
from service.preprocessing.data_preprocessing import do_preprocessing
from service.preprocessing.create_feature import size_type_last, rel_major

class PredictionService:
    """모델 로드 및 예측 서비스 클래스"""
    
    def __init__(self, model_path: str = "Data/models/model.pkl"):
        self.model_path = model_path
        self.model = None
        self.training_columns = None
        self.columns_path = model_path.replace('.pkl', '_columns.pkl')
        
    def load_model(self) -> bool:
        """저장된 모델을 로드"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"모델이 성공적으로 로드되었습니다: {self.model_path}")
                
                # 훈련 데이터의 컬럼 정보 로드
                self._load_training_columns()
                return True
            else:
                print(f"모델 파일이 존재하지 않습니다: {self.model_path}")
                return False
        except Exception as e:
            print(f"모델 로드 중 오류 발생: {e}")
            return False
    
    def _load_training_columns(self):
        """훈련 시 사용된 컬럼 정보 로드"""
        if os.path.exists(self.columns_path):
            try:
                with open(self.columns_path, 'rb') as f:
                    self.training_columns = pickle.load(f)
                logging.info(f"저장된 컬럼 파일에서 로드: {len(self.training_columns)}개 컬럼")
                return
            except Exception as e:
                logging.warning(f"저장된 컬럼 파일 로드 실패: {e}")
    
    def _save_training_columns(self):
        """훈련 컬럼 정보를 파일로 저장"""
        try:
            with open(self.columns_path, 'wb') as f:
                pickle.dump(self.training_columns, f)
            logging.info(f"컬럼 정보 저장 완료: {self.columns_path}")
        except Exception as e:
            logging.warning(f"컬럼 정보 저장 실패: {e}")

    def _apply_basic_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """기본 전처리: 한글 매핑 및 기본값 설정"""
        df = df.copy()
        
        # 전체 데이터에서 "정보없음" → NaN으로 변환
        df = df.replace("정보없음", np.nan).infer_objects(copy=False)
        
        # 한글 매핑
        company_size_mapping = {
            '10명 이하': '<10',
            '10명 ~ 49명': '10/49', 
            '50명 ~ 99명': '50-99',
            '100명 ~ 499명': '100-500',
            '500명 ~ 999명': '500-999',
            '1000명 ~ 4999명': '1000-4999',
            '5000명 ~ 9999명': '5000-9999',
            '10000명 이상': '10000+'
        }

        last_new_job_mapping = {
            '1년': '1', '2년': '2', '3년': '3', '4년': '4', '4년 이상': '>4', 'never': 'never'
        }

        if 'company_size' in df.columns:
            df['company_size'] = df['company_size'].map(company_size_mapping).fillna(df['company_size']).infer_objects(copy=False)

        if 'last_new_job' in df.columns:
            df['last_new_job'] = df['last_new_job'].map(last_new_job_mapping).fillna(df['last_new_job']).infer_objects(copy=False)

        # training_hours 기본값 추가
        if 'training_hours' not in df.columns:
            df['training_hours'] = 50

        return df

    def _align_with_reference(self, df: pd.DataFrame, reference_columns: list, fill_value=0) -> pd.DataFrame:
        """DataFrame을 참조 컬럼 리스트와 동일하게 정렬"""
        df_aligned = df.copy()
        
        # 누락된 컬럼 추가
        missing_cols = set(reference_columns) - set(df_aligned.columns)
        for col in missing_cols:
            df_aligned[col] = fill_value
        
        # 참조 컬럼과 동일한 순서로 정렬
        df_aligned = df_aligned.reindex(columns=reference_columns, fill_value=fill_value)
        
        return df_aligned
    
    def preprocess_input(self, user_input: dict) -> pd.DataFrame:
        """
        기존 전처리 모듈을 활용한 사용자 입력 전처리
        """
        try:
            # 1. DataFrame으로 변환
            df = pd.DataFrame([user_input])
            
            # 2. 기본 전처리 적용 (한글 매핑, 기본값 설정)
            df = self._apply_basic_preprocessing(df)
            
            # 3. 더미 train 데이터 생성 - 동일한 데이터로 시작
            df_dummy_train = df.copy()
            df_test = df.copy()
            
            # 4. Feature Engineering - 기존 create_feature.py 함수들 사용
            df_dummy_train, df_test = size_type_last(df_dummy_train, df_test)
            df_dummy_train, df_test = rel_major(df_dummy_train, df_test)
            
            # job_size_type_group 컬럼 제거 (모델 입력에 불필요한 라벨 컬럼)
            for df_temp in [df_dummy_train, df_test]:
                if "job_size_type_group" in df_temp.columns:
                    df_temp.drop(columns=["job_size_type_group"], inplace=True)
            
            # 코드 컬럼들을 int32로 변환
            for c in ["job_size_type_code", "rel_major_code"]:
                for df_temp in [df_dummy_train, df_test]:
                    if c in df_temp.columns:
                        df_temp[c] = df_temp[c].astype("int32")
            
            # 5. 전처리 파이프라인
            drop_cols = []  
            transform_cols = [] 
            encoding_cols = [
                'relevent_experience', 'enrolled_university', 'education_level',
                'major_discipline', 'experience', 'company_size',
                'company_type', 'last_new_job'
            ]
            
            # 컬럼 수 확인
            print(f"\n전처리 전 - dummy_train 컬럼 수: {df_dummy_train.shape[1]}, test 컬럼 수: {df_test.shape[1]}")
            print(f"\n전처리 전 - dummy_train 컬럼: {list(df_dummy_train.columns)}")
            print(f"\n전처리 전 - test 컬럼: {list(df_test.columns)}")
            
            df_dummy_train, df_processed = do_preprocessing(
                df_dummy_train, df_test, drop_cols, transform_cols, encoding_cols
            )
            
            # 6. 학습 시 사용한 컬럼과 정렬
            if self.training_columns:
                df_processed = self._align_with_reference(
                    df_processed, self.training_columns, fill_value=0
                )
                logging.info(f"\n컬럼 정렬 완료: {df_processed.shape[1]}개 특성")
            else:
                logging.warning("\n훈련 컬럼 정보가 없어 정렬을 건너뜁니다.")
            
            print(f"\n전처리된 데이터 shape: {df_processed.shape}")
            print(f"\n전처리된 데이터 컬럼: {list(df_processed.columns)}")
            
            return df_processed
            
        except Exception as e:
            logging.error(f"전처리 중 오류 발생: {e}")
            raise

    def predict(self, user_input: dict) -> float:
        """사용자 입력에 대한 예측을 수행"""
        if self.model is None:
            if not self.load_model():
                raise Exception("모델 로드 실패")
        
        try:
            # 전처리
            df_processed = self.preprocess_input(user_input)
            
            # 예측 실행
            prediction_proba = self.model.predict_proba(df_processed)
            print(f"\n예측 결과 shape: {prediction_proba.shape}")
            
            # 클래스 1 (합류할 확률)의 확률 반환
            probability = prediction_proba[0, 1]
            print(f"\n최종 예측 확률: {probability}")
            
            return float(probability)
            
        except Exception as e:
            logging.error(f"예측 중 오류 발생: {e}")
            raise


prediction_service = PredictionService()

def get_prediction(user_input: dict) -> float:
    """편의 함수: 사용자 입력에 대한 예측 확률을 반환"""
    return prediction_service.predict(user_input)