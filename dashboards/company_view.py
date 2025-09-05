import streamlit as st
import pandas as pd

df = pd.read_csv("Data/predictions_and_target.csv")

def show():
    st.title("company view")

    important_columns = ["relevent_experience", "enrolled_university", "education_level", "major_discipline", "experience", "company_size", "company_type", "last_new_job", "prediction_probability"]

    random_df = df[important_columns] # 중요 컬럼 몇개만 뽑아서 

    random_df['prediction_probability'] = random_df['prediction_probability'].apply(
        lambda x: '🟢' 
        if x >= 0.7 else '🟡' 
        if x >= 0.4 else '🔴'
    )

    # prediction의 값이 🟢인 개수 count
    green_count = random_df[random_df['prediction_probability'] == '🟢'].shape[0]
    yellow_count = random_df[random_df['prediction_probability'] == '🟡'].shape[0]
    red_count = random_df[random_df['prediction_probability'] == '🔴'].shape[0]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"🟢(70%이상): {green_count}")
    with col2:
        st.write(f"🟡(40%이상): {yellow_count}")
    with col3:
        st.write(f"🔴(40%미만): {red_count}")

    st.dataframe(random_df)

def graph1_show():
    st.title("취업준비생의 당사 회사 합류 비율")
    # company_size: nan이고 company_type:nan이고 last_new_job: never인 데이터 추출 -> 취업 준비생
    nan_df = df[df['company_size'].isna() & df['company_type'].isna() &( df['last_new_job'] == 'never')]
    # 취업 준비생의 회사 합류 비율 그래프
    st.bar_chart(nan_df['target'].value_counts())

    st.title("이직준비생의 당사 회사 합류 비율")
    # company_size: nan이고 company_type:nan이고 last_new_job: nan도 아니고 never도 아닌 데이터 추출 -> 이직 준비생
    nan_df = df[df['company_size'].isna() & df['company_type'].isna() &( df['last_new_job'] != 'never') & (df['last_new_job'] != 'nan')]
    # 이직 준비생의 회사 합류 비율 그래프
    st.bar_chart(nan_df['target'].value_counts())

    st.title("현업자의 당사 회사 합류 비율")
    # company_size: nan이 아니거나 company_type: nan이 아니거나 last_new_job: nan도 아니고 never도 아닌 데이터 추출 -> 현업자
    nan_df = df[df['company_size'].notna() | df['company_type'].notna() | (( df['last_new_job'] != 'never') & (df['last_new_job'] != 'nan'))]
    # 현업자의 회사 합류 비율 그래프
    st.bar_chart(nan_df['target'].value_counts())





def graph2_show():
    st.title("최종학력에 따른 당사 회사 합류 비율")
    # 최종학력별 회사합류 비율
    st.bar_chart(df['education_level'].value_counts())

    st.title("학교재학상태에 따른 당사 회사 합류 비율")
    # 학교재학상태별 회사합류 비율
    st.bar_chart(df['enrolled_university'].value_counts())


def graph3_show():
    st.title("경력에 따른 당사 회사 합류 비율")
    # 경력별 회사합류 비율
    st.bar_chart(df['experience'].value_counts())

    st.title("교육시간에 따른 당사 회사 합류 비율")
    # 교육시간별 회사합류 비율
    st.bar_chart(df['training_hours'].value_counts())