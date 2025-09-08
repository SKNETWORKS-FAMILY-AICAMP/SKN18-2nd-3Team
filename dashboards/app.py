import streamlit as st
import company_view
import candidate_view
import pandas as pd
from streamlit_option_menu import option_menu

df = pd.read_csv("./result_csv/result_test.csv")

st.set_page_config(layout="wide")

# --- 사이드바 메인 메뉴 ---
with st.sidebar:
    st.markdown(
        "<h4 style='font-size:13px; color:#243746; margin-bottom:5px;'>Menu</h4>",
        unsafe_allow_html=True
    )

    menu = option_menu(
        None,
        ['Company', 'Candidate'],
        icons=['building', 'person-badge'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#243746", "font-size": "16px"},
            "nav-link": {
                "font-size": "13px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#ef494c"},
        }
    )

# --- 메인 내용 ---
if menu == "Company":
    company_view.info_show()

    with st.sidebar:
        st.markdown(
            "<h4 style='font-size:12px; color:#243746; margin-bottom:3px;'>세부 분석</h4>",
            unsafe_allow_html=True
        )

        sub_menu = option_menu(
            None,  
            ["취업 경력에 따른 당사 입사 가능성", "지원자의 학력", "지원자의 전공 Level"],
            icons=['graph-up', 'mortarboard-fill', 'journals'],
            menu_icon="caret-down-fill",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#243746", "font-size": "14px"},
                "nav-link": {
                    "font-size": "12px",  
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#ef494c"},
            }
        )

    if sub_menu == "취업 경력에 따른 당사 입사 가능성":
        company_view.graph1_show()
        company_view.show()
    elif sub_menu == "지원자의 학력":
        company_view.graph2_show()
        company_view.show()
    elif sub_menu == "지원자의 전공 Level":
        company_view.graph3_show()
        company_view.show()

elif menu == "Candidate":
    candidate_view.show()
