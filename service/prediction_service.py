import pickle
import pandas as pd
import numpy as np
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class PredictionService:
    """모델 로드 및 예측 서비스 클래스"""
    
    def __init__(self, model_path: str = "Data/models/model.pkl"):
        self.model_path = model_path
        self.model = None
        self.training_columns = None
        self.columns_path = model_path.replace('.pkl', '_columns.pkl')
    
    def load_model(self) -> bool:
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logging.info(f"모델이 성공적으로 로드되었습니다: {self.model_path}")
                self._load_training_columns()
                return True
            else:
                logging.error(f"모델 파일이 존재하지 않습니다: {self.model_path}")
                return False
        except Exception as e:
            logging.error(f"모델 로드 중 오류 발생: {e}")
            return False
    
    def _load_training_columns(self):
        if os.path.exists(self.columns_path):
            try:
                with open(self.columns_path, 'rb') as f:
                    self.training_columns = pickle.load(f)
                logging.info(f"저장된 컬럼 파일에서 로드: {len(self.training_columns)}개 컬럼")
            except Exception as e:
                logging.warning(f"저장된 컬럼 파일 로드 실패: {e}")
    
    def _save_training_columns(self):
        try:
            with open(self.columns_path, 'wb') as f:
                pickle.dump(self.training_columns, f)
            logging.info(f"컬럼 정보 저장 완료: {self.columns_path}")
        except Exception as e:
            logging.warning(f"컬럼 정보 저장 실패: {e}")

    def _apply_basic_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.replace("정보없음", np.nan)

        company_size_mapping = {
            '10명 이하': '<10', '10명 ~ 49명': '10/49', 
            '50명 ~ 99명': '50-99', '100명 ~ 499명': '100-500',
            '500명 ~ 999명': '500-999', '1000명 ~ 4999명': '1000-4999',
            '5000명 ~ 9999명': '5000-9999', '10000명 이상': '10000+'
        }
        last_new_job_mapping = {
            '1년': '1', '2년': '2', '3년': '3', '4년': '4',
            '4년 이상': '>4', 'never': 'never'
        }

        if 'company_size' in df.columns:
            df['company_size'] = df['company_size'].map(company_size_mapping).fillna(df['company_size'])
        if 'last_new_job' in df.columns:
            df['last_new_job'] = df['last_new_job'].map(last_new_job_mapping).fillna(df['last_new_job'])

        if 'training_hours' not in df.columns:
            df['training_hours'] = 270  # 기본값
        return df

    def _do_single_encoding(self, df: pd.DataFrame, encoding_cols: list) -> pd.DataFrame:
        df_encoded = df.copy()
        existing_cols = [col for col in encoding_cols if col in df_encoded.columns]
        if existing_cols:
            df_encoded = pd.get_dummies(df_encoded, columns=existing_cols, drop_first=False)
            df_encoded.columns = [c.replace(" ", "_") for c in df_encoded.columns]
        return df_encoded

    def _align_with_reference(self, df: pd.DataFrame, reference_columns: list, fill_value=0) -> pd.DataFrame:
        df_aligned = df.copy()
        missing_cols = set(reference_columns) - set(df_aligned.columns)
        for col in missing_cols:
            df_aligned[col] = fill_value
        return df_aligned.reindex(columns=reference_columns, fill_value=fill_value)

    def _create_additional_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        def _classify(row):
            cs_nan = pd.isna(row.get("company_size"))
            ct_nan = pd.isna(row.get("company_type"))
            lnj = row.get("last_new_job")
            if cs_nan and ct_nan:
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
            "No Response": 0, "New Graduate": 1, "Experienced Unemployed": 2,
            "Other_NoResponse": 3, "Other_NewGraduate": 4,
            "Other_Experienced": 5, "Complete": 6,
        }
        df["job_size_type_code"] = df["job_size_type_group"].map(group2code).fillna(6).astype(int)

        def norm_rel(x):
            if pd.isna(x): return np.nan
            s = str(x).strip().lower()
            if s.startswith("has"): return "Has"
            if s.startswith("no"): return "No"
            return s

        if "major_discipline" in df.columns:
            major_col = "major_discipline"
        elif "major_dicipline" in df.columns:
            major_col = "major_dicipline"
        else:
            major_col = None

        if major_col:
            rel_txt = df["relevent_experience"].apply(norm_rel)
            major_txt = df[major_col].astype("string")
            df["rel_major_code"] = rel_txt.astype("string").str.cat(major_txt, sep="|", na_rep="NA")
        else:
            df["rel_major_code"] = "Unknown"
        return df

    def preprocess_input(self, user_input: dict) -> pd.DataFrame:
        try:
            df = pd.DataFrame([user_input])
            logging.debug(f"[원본 입력값] {df.to_dict(orient='records')[0]}")

            df = self._apply_basic_preprocessing(df)
            logging.debug(f"[기본 전처리 후] {df.to_dict(orient='records')[0]}")

            df = self._create_additional_features(df)
            logging.debug(f"[파생 변수 생성 후] {df.to_dict(orient='records')[0]}")

            encoding_cols = [
                'relevent_experience', 'enrolled_university', 'education_level',
                'major_discipline', 'experience', 'company_size',
                'company_type', 'last_new_job',
                'rel_major_code', 'job_size_type_code', 'exp_bin_code'
            ]
            df_encoded = self._do_single_encoding(df, encoding_cols)
            logging.debug(f"[원핫 인코딩 후] {df_encoded.head(1).to_dict()}")

            if self.training_columns:
                df_encoded = self._align_with_reference(df_encoded, self.training_columns, fill_value=0)
                logging.info(f"컬럼 정렬 완료: {df_encoded.shape[1]}개 특성")
            else:
                logging.warning("훈련 컬럼 정보가 없어 정렬을 건너뜁니다.")

            logging.debug(f"[최종 입력 벡터 shape] {df_encoded.shape}")
            logging.debug(f"[최종 입력 벡터 값 일부] {df_encoded.iloc[0].to_dict()}")

            return df_encoded
        except Exception as e:
            logging.error(f"전처리 중 오류 발생: {e}")
            raise

    def predict(self, user_input: dict) -> float:
        if self.model is None:
            if not self.load_model():
                raise Exception("모델 로드 실패")

        try:
            df_processed = self.preprocess_input(user_input)
            prediction_proba = self.model.predict_proba(df_processed)

            if hasattr(self.model, "feature_importances_"):
                fi = pd.DataFrame({
                    "feature": df_processed.columns,
                    "importance": self.model.feature_importances_
                }).sort_values(by="importance", ascending=False)
                logging.info("=== [상위 20개 중요 Feature] ===")
                logging.info("\n" + fi.head(20).to_string(index=False))

            probability = prediction_proba[0, 1]
            logging.info(f"최종 예측 확률: {probability:.12f}")
            return float(probability)
        except Exception as e:
            logging.error(f"예측 중 오류 발생: {e}")
            raise


# 전역 서비스
prediction_service = PredictionService()

def get_prediction(user_input: dict) -> float:
    return prediction_service.predict(user_input)
