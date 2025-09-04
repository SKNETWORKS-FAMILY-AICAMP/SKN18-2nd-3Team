import streamlit as st
import pandas as pd

df = pd.read_csv("Data/test_predictions.csv")

def show():
    st.title("company view")

    important_columns = ["relevent_experience", "enrolled_university", "education_level", "major_discipline", "experience", "company_size", "company_type", "last_new_job", "prediction"]

    random_df = df[important_columns] # 중요 컬럼 몇개만 뽑아서 

    random_df['prediction'] = random_df['prediction'].apply(
        lambda x: '🟢' 
        if x >= 0.7 else '🟡' 
        if x >= 0.4 else '🔴'
    )

    # prediction의 값이 🟢인 개수 count
    green_count = random_df[random_df['prediction'] == '🟢'].shape[0]
    yellow_count = random_df[random_df['prediction'] == '🟡'].shape[0]
    red_count = random_df[random_df['prediction'] == '🔴'].shape[0]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"🟢(70%이상): {green_count}")
    with col2:
        st.write(f"🟡(40%이상): {yellow_count}")
    with col3:
        st.write(f"🔴(40%미만): {red_count}")

    st.dataframe(random_df)

def graph1_show():
    st.title("취업준비생/이직준비생/현업자 의 당사 회사 합류 비율")
    # company_size: nan이고 company_type:nan이고 last_new_job: never인 데이터 추출 -> 취업 준비생
    nan_df = df[df['company_size'].isna() & df['company_type'].isna() & df['last_new_job'] == 'never']



def graph2_show():
    st.title("전공")

def graph3_show():
    st.title("분석 그래프3")