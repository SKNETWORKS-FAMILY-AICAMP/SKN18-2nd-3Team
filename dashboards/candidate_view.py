import streamlit as st
import pandas as pd
import os
import sys

# 상위 디렉토리의 service 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from service.prediction_service import get_prediction

def show():
    st.title("지원자 프로필 진단하기") 
    st.markdown("---")
    
    st.markdown("""
    ### 📝 개인 정보를 입력해주세요
    
    입력하신 정보를 바탕으로 **우리 회사 합류 가능성**을 분석해드립니다.
    
    **분석 결과 해석:**
    - **높은 점수 (60% 이상) **: 합류 가능성 매우 높음
    - **보통 점수 (20-60%) **: 합류 가능성 보통
    - **낮은 점수 (20% 미만) **: 합류 가능성 낮음
    """)

    with st.form("candidate_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("교육 및 경력")
            relevent_experience = st.selectbox(
                "관련 경험 유무", 
                ['Has relevent experience', 'No relevent experience', '정보없음'],
            )
            enrolled_university = st.selectbox(
                "대학교 등록 상태", 
                ['no_enrollment', 'Full time course', 'Part time course', '정보없음'],
            )
            education_level = st.selectbox(
                "최종 학력", 
                ['Graduate', 'Masters', 'High School', 'Phd', 'Primary School', '정보없음'],
            )
            major_discipline = st.selectbox(
                "전공 분야",
                ['STEM', 'Business Degree', 'Arts', 'Humanities', 'No Major', 'Other', '정보없음'],
            )
            
        with col2:
            st.subheader("직장 정보")
            experience = st.selectbox(
                "총 경력 (년)", 
                ['<1', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '>20','정보없음'],
            )
            company_size = st.selectbox(
                "현재 회사 규모", 
                ["10명 이하", "10명 ~ 49명", "50명 ~ 99명", "100명 ~ 500명", "500명 ~ 999명", "1000명 ~ 4999명", "5000명 ~ 9999명", "10000+", "정보없음"],
            )
            company_type = st.selectbox(
                "회사 유형", 
                ["Pvt Ltd", "Funded Startup", "Early Stage Startup", "Other", "Public Sector", "NGO", "정보없음"],
            )
            last_new_job = st.selectbox(
                "마지막 이직 시기", 
                ["1년", "2년", "3년", "4년", "4년 이상", "never", "정보없음"],
            )
        
        st.markdown("---")
        submitted = st.form_submit_button("합류 가능성 진단하기", use_container_width=True)

        if submitted:
            user_input = {
                "relevent_experience": relevent_experience,
                "enrolled_university": enrolled_university, 
                "education_level": education_level,
                "major_discipline": major_discipline,
                "experience": experience,
                "company_size": company_size,
                "company_type": company_type,
                "last_new_job": last_new_job
            }
            
            # 예측 실행
            with st.spinner('모델 예측중'):
                try:
                    prediction_prob = get_prediction(user_input)
                    # 예측값이 올바른 형태인지 확인
                    if prediction_prob is None:
                        prediction_prob = 0.0
                    elif not isinstance(prediction_prob, (int, float)):
                        prediction_prob = 0.0
                    # 0~1 범위로 제한
                    prediction_prob = max(0.0, min(1.0, float(prediction_prob)))
                except Exception as e:
                    st.error(f"예측 중 오류가 발생했습니다: {str(e)}")
                    prediction_prob = 0.0
            
            # 결과 표시
            st.markdown("---")
            st.markdown("## 진단 결과")
            
            # 메트릭 표시
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="회사 합류 가능성", 
                    value=f"{prediction_prob:.1%}",
                )
            
            with col2:
                if prediction_prob >= 0.6:
                    join_level = "매우 높음"
                    level_icon = "🟢"
                elif prediction_prob >= 0.2:
                    join_level = "보통"
                    level_icon = "🟠"
                else:
                    join_level = "낮음"
                    level_icon = "🔴"
                
                st.metric(
                    label="합류 가능성 수준", 
                    value=f"{level_icon} {join_level}",
                )
            
            # 진행률 바
            st.markdown("### 회사 합류 가능성 지수")
            st.progress(float(prediction_prob))
            
            # 결과 해석 추가
            st.markdown("---")
            st.markdown("### 결과 해석")
            
            if prediction_prob >= 0.6:
                st.success("""
                **** 
                """)
            elif prediction_prob >= 0.3:
                st.warning("""
                **** 
                """)
            else:
                st.error("""
                **** 
                """)
            
            with st.expander("입력된 정보"):
                input_df = pd.DataFrame([user_input])
                st.dataframe(input_df, use_container_width=True)
            