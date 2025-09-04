import streamlit as st
import company_view
import candidate_view

st.set_page_config(layout="wide") # 레이아웃 넓게

col1, col2, col3 = st.columns([1,3,1])

with col2:
    tab1, tab2 = st.tabs(["Company", "Candidate"])
    with tab1:
        company_view.show()
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["분석 그래프1", "분석 그래프2", "분석 그래프3"])
        with sub_tab1:
            company_view.graph1_show()
        with sub_tab2:
            company_view.graph2_show()
        with sub_tab3:
            company_view.graph3_show()
    with tab2:
        candidate_view.show()
