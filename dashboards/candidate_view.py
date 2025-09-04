import streamlit as st
import pandas as pd

def show():
    st.title("내 프로필 진단하기") 

    # 모델 load 하기

    with st.form("candidate_form"):
    # 사용자의 정보 입력 받기
        relevent_experience = st.selectbox("relevent_experience", ['Has relevent experience', 'No relevent experience'])
        enrolled_university = st.selectbox("enrolled_university", ['no_enrollment', 'Full time course', 'Part time course'])
        education_level = st.selectbox("education_level", ['Graduate', 'Masters', 'High School', 'Phd', 'Primary School'])
        experience = st.selectbox("experience", ['>20', '15', '5', '<1', '11', '13', '7', '17', '2', '16', '1', '4', '10', '14', '18', '19', '12', '3', '6', '9', '8', '20'])
        company_size = st.selectbox("company_size", ["10명 이하", "10명 ~ 49명", "50명 ~ 99명", "100명 ~ 500명", "500명 ~ 999명", "1000명 ~ 4999명", "5000명 ~ 9999명", "10000+"])
        company_type = st.selectbox("company_type", ["Pvt Ltd", "Funded Startup", "Early Stage Startup", "Other", "Public Sector", "NGO"])
        last_new_job = st.selectbox("last_new_job", ["1년", "2년", "3년", "4년","4년 이상"])

        if st.form_submit_button("진단하기"):
            input_df = pd.DataFrame([
                [relevent_experience, enrolled_university, education_level, experience, company_size, company_type, last_new_job]
            ], columns=["relevent_experience", "enrolled_university", "education_level", "experience", "company_size", "company_type", "last_new_job"])

            # 나중에 모델 연결하고 예측 결과 보여주는걸로 바꾸기
            st.write(input_df)