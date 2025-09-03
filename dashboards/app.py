import streamlit as st
import company_view
import candidate_view

tab1, tab2 = st.tabs(["Company", "Candidate"])
with tab1:
    company_view.show()
with tab2:
    candidate_view.show()
