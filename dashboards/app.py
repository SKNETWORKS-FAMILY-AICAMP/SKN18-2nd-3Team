import streamlit as st
import company_view
import candidate_view
import pandas as pd

df = pd.read_csv("./result_csv/result_test.csv")

st.set_page_config(layout="wide") # 레이아웃 넓게

col1, col2, col3 = st.columns([1,3,1])

with col2:
    tab1, tab2 = st.tabs(["Company", "Candidate"])


    with tab1:
        company_view.info_show()
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["취업 경력에 따른 당사 입사 가능성", "지원자의 학력", "지원자의 전공 Level"])
        with sub_tab1:
            company_view.graph1_show()
            company_view.show()
        with sub_tab2:
            company_view.graph2_show()
            company_view.show()
        with sub_tab3:
            company_view.graph3_show()
            company_view.show()
    with tab2:
        candidate_view.show()
