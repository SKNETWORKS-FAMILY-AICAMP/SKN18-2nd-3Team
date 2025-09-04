import streamlit as st
import pandas as pd

def show():
    st.title("회사 관점 입니다!")

    df = pd.read_csv("Data/test_predictions.csv")

    important_columns = ["relevent_experience", "enrolled_university", "education_level", "experience", "company_size", "company_type", "last_new_job", "prediction"]

    filtered_df = df[important_columns] # 중요 컬럼 몇개만 뽑아서 
    random_df = filtered_df.sample(n=30) # 랜덤 30개

    random_df['prediction'] = random_df['prediction'].apply(
        lambda x: '🟢' 
        if x >= 0.7 else '🟡' 
        if x >= 0.4 else '🔴'
    )
    st.dataframe(random_df)

def graph1_show():
    st.title("분석 그래프1")

def graph2_show():
    st.title("분석 그래프2")

def graph3_show():
    st.title("분석 그래프3")