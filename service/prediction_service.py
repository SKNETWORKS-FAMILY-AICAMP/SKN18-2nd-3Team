<<<<<<< HEAD
import pickle
import pandas as pd
import numpy as np
import os
import logging

class PredictionService:
    """모델 로드 및 예측 서비스 클래스"""
    
    def __init__(self, model_path: str = "Data/models/model.pkl"):
        self.model_path = model_path
        self.model = None
        self.training_columns = None
        self.columns_path = model_path.replace('.pkl', '_columns.pkl')  # 컬럼 정보 파일 경로
        
    def load_model(self) -> bool:
        """
        저장된 모델을 로드

        """
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
        """
        훈련 시 사용된 컬럼 정보로드

        """
        if os.path.exists(self.columns_path):
            try:
                with open(self.columns_path, 'rb') as f:
                    self.training_columns = pickle.load(f)
                logging.info(f"저장된 컬럼 파일에서 로드: {len(self.training_columns)}개 컬럼")
                return
            except Exception as e:
                logging.warning(f"저장된 컬럼 파일 로드 실패: {e}")
    
    def _save_training_columns(self):
        """
        훈련 컬럼 정보를 파일로 저장
        """
        try:
            with open(self.columns_path, 'wb') as f:
                pickle.dump(self.training_columns, f)
            logging.info(f"컬럼 정보 저장 완료: {self.columns_path}")
        except Exception as e:
            logging.warning(f"컬럼 정보 저장 실패: {e}")

    def _preprocess_sample_for_columns(self, sample_input: dict) -> pd.DataFrame:
        """
        컬럼 구조 파악을 위한 전처리
        """
        df = pd.DataFrame([sample_input])
        
        # 기본 전처리 적용
        df = self._apply_basic_preprocessing(df)
        
        # Feature Engineering 적용
        df = self._create_additional_features(df)
        
        # 인코딩 적용
        encoding_cols = [
            'relevent_experience', 'enrolled_university', 'education_level',
            'major_discipline', 'experience', 'company_size',
            'company_type', 'last_new_job',
            'rel_major_code', 'job_size_type_code', 'exp_bin_code'
        ]
        df_encoded = self._do_single_encoding(df, encoding_cols)
        
        return df_encoded

    def _apply_basic_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # 전체 데이터에서 "정보없음" → NaN으로 변환
        df = df.replace("정보없음", np.nan)

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
            df['company_size'] = df['company_size'].map(company_size_mapping).fillna(df['company_size'])

        if 'last_new_job' in df.columns:
            df['last_new_job'] = df['last_new_job'].map(last_new_job_mapping).fillna(df['last_new_job'])

        # training_hours 기본값 추가
        if 'training_hours' not in df.columns:
            df['training_hours'] = 40

        return df


    def _do_single_encoding(self, df: pd.DataFrame, encoding_cols: list) -> pd.DataFrame:
        """
        단일 DataFrame에 대한 원핫 인코딩
        """
        df_encoded = df.copy()
        
        # 존재하는 컬럼만 인코딩
        existing_cols = [col for col in encoding_cols if col in df_encoded.columns]
        
        if existing_cols:
            df_encoded = pd.get_dummies(df_encoded, columns=existing_cols)
        
        return df_encoded

    def _align_with_reference(self, df: pd.DataFrame, reference_columns: list, fill_value=0) -> pd.DataFrame:
        """
        DataFrame을 참조 컬럼 리스트와 동일하게 정렬
        """
        df_aligned = df.copy()
        
        # 누락된 컬럼 추가
        missing_cols = set(reference_columns) - set(df_aligned.columns)
        for col in missing_cols:
            df_aligned[col] = fill_value
        
        # 참조 컬럼과 동일한 순서로 정렬
        df_aligned = df_aligned.reindex(columns=reference_columns, fill_value=fill_value)
        
        return df_aligned
    
    def _create_additional_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        size_type_last, rel_major 기반의 파생 특성 생성
        """
        df = df.copy()

        # -------------------------
        # 1. 회사 규모 + 유형 + 마지막 이직 (size_type_last)
        # -------------------------
        def _classify(row):
            cs_nan = pd.isna(row.get("company_size"))
            ct_nan = pd.isna(row.get("company_type"))
            lnj = row.get("last_new_job")

            if cs_nan and ct_nan:  # 둘 다 NaN
                if pd.isna(lnj):
                    return "No Response"
                elif lnj == "never":
                    return "New Graduate"
                else:
                    return "Experienced Unemployed"
            else:
                return "Complete"

        df["job_size_type_group"] = df.apply(_classify, axis=1)

        group2code = {
            "No Response": 0,
            "New Graduate": 1,
            "Experienced Unemployed": 2,
            "Other_NoResponse": 3,
            "Other_NewGraduate": 4,
            "Other_Experienced": 5,
            "Complete": 6,
        }
        df["job_size_type_code"] = df["job_size_type_group"].map(group2code).fillna(6).astype(int)

        # -------------------------
        # 2. 관련 경험 × 전공 (rel_major)
        # -------------------------
        def norm_rel(x):
            if pd.isna(x):
                return np.nan
            s = str(x).strip().lower()
            if s.startswith("has"):
                return "Has"
            if s.startswith("no"):
                return "No"
            return s

        # major_discipline 컬럼 선택 (혹시 dicipline 오타 대응)
        if "major_discipline" in df.columns:
            major_col = "major_discipline"
        elif "major_dicipline" in df.columns:
            major_col = "major_dicipline"
        else:
            major_col = None

        if major_col:
            rel_txt = df["relevent_experience"].apply(norm_rel)
            major_txt = df[major_col].astype("string")
            cross_txt = rel_txt.astype("string").str.cat(major_txt, sep="|", na_rep="NA")
            df["rel_major_code"] = cross_txt
        else:
            df["rel_major_code"] = "Unknown"

        return df

    
    def _convert_experience_to_number(self, experience_str: str) -> float:
        """
        경험 문자열을 숫자로 변환
        """
        if experience_str == '<1':
            return 0.5
        elif experience_str == '>20':
            return 22.0
        else:
            try:
                return float(experience_str)
            except:
                return 5.0  # 기본값
    
    def preprocess_input(self, user_input: dict) -> pd.DataFrame:
        """
        사용자 입력을 전처리
        """
        try:
            # 1. DataFrame으로 변환
            df = pd.DataFrame([user_input])
            
            # 2. 기본 전처리 적용 (모듈화된 함수 사용)
            df = self._apply_basic_preprocessing(df)
            
            # 2.5. Feature Engineering 적용
            df = self._create_additional_features(df)
            
            # 3. preprocessing 모듈의 인코딩 함수 사용 (범주형만 인코딩)
            encoding_cols = [
                'relevent_experience', 'enrolled_university', 'education_level',
                'major_discipline', 'experience', 'company_size',
                'company_type', 'last_new_job',
                'rel_major_code', 'job_size_type_code', 'exp_bin_code' 
            ]
            df_encoded = self._do_single_encoding(df, encoding_cols)
            
            if self.training_columns:
                df_encoded = self._align_with_reference(df_encoded, self.training_columns, fill_value=0)
                logging.info(f"컬럼 정렬 완료: {df_encoded.shape[1]}개 특성")
            else:
                logging.warning("훈련 컬럼 정보가 없어 정렬을 건너뜁니다.")
            
            print(f"전처리된 데이터 shape: {df_encoded.shape}")
            print(f"전처리된 데이터 컬럼: {list(df_encoded.columns)}")
            
            return df_encoded
            
        except Exception as e:
            logging.error(f"전처리 중 오류 발생: {e}")
            raise

    def predict(self, user_input: dict) -> float:
        """
        사용자 입력에 대한 예측을 수행
        """
        # 모델이 로드되지 않았다면 로드 시도
        if self.model is None:
            if not self.load_model():
                raise Exception("모델 로드 실패")
        
        try:
            # 전처리
            df_processed = self.preprocess_input(user_input)
            
            # 예측 실행
            prediction_proba = self.model.predict_proba(df_processed)
            print(f"예측 결과 shape: {prediction_proba.shape}")
            
            # 클래스 1 (합류할 확률)의 확률 반환
            probability = prediction_proba[0, 1]  # 두 번째 클래스 (target=1)의 확률
            print(f"최종 예측 확률: {probability}")
            
            return float(probability)
            
        except Exception as e:
            logging.error(f"예측 중 오류 발생: {e}")
            raise


# 전역 서비스 
prediction_service = PredictionService()

def get_prediction(user_input: dict) -> float:
    """
    편의 함수: 사용자 입력에 대한 예측 확률을 반환
    """
    return prediction_service.predict(user_input)