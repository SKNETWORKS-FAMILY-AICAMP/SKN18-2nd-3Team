import streamlit as st
import pandas as pd
import os, sys

# 상위 디렉토리 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.prediction_service import get_prediction

def show():
    # 헤더
    st.markdown(
        """
        <h1 style="text-align:center; color:#2E86C1;">지원자 프로필 진단</h1>
        <p style="text-align:center; font-size:18px;">입력한 정보를 기반으로 <b>회사 합류 가능성</b>을 예측합니다.</p>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    # 안내
    st.info(
        """
        **결과 해석 가이드**
        - 🟢 **높음 (60% 이상):** 합류 가능성 매우 높음  
        - 🟠 **보통 (20% ~ 60%):** 합류 가능성 보통  
        - 🔴 **낮음 (20% 미만):** 합류 가능성 낮음
        """,
        icon="ℹ️"
    )

    # -----------------------------
    # 매핑 딕셔너리
    # -----------------------------
    relevent_experience_map = {
        "관련 경험 있음": "Has relevent experience",
        "관련 경험 없음": "No relevent experience",
        "정보 없음": None
    }
    enrolled_university_map = {
        "전일제 과정": "Full time course",
        "미등록": "no_enrollment",
        "시간제 과정": "Part time course",
        "정보 없음": None
    }
    education_level_map = {
        "대졸": "Graduate",
        "고등학교 졸업": "High School",
        "석사": "Masters",
        "박사": "Phd",
        "초등학교 졸업": "Primary School",
        "정보 없음": None
    }
    major_discipline_map = {
        "이공계(STEM)": "STEM",
        "경영학": "Business Degree",
        "예술": "Arts",
        "인문학": "Humanities",
        "전공 없음": "No Major",
        "기타": "Other",
        "정보 없음": None
    }
    experience_map = (
        {"1년 미만": "<1"} |
        {f"{i}년": str(i) for i in range(1, 21)} |
        {">20년": ">20", "정보 없음": None}
    )
    company_size_map = {
        "10명 이하": "<10",
        "10~49명": "10/49",
        "50~99명": "50-99",
        "100~500명": "100-500",
        "500~999명": "500-999",
        "1000~4999명": "1000-4999",
        "5000~9999명": "5000-9999",
        "10000명 이상": "10000+",
        "정보 없음": None
    }
    company_type_map = {
        "개인기업(Pvt Ltd)": "Pvt Ltd",
        "투자받은 스타트업": "Funded Startup",
        "초기 스타트업": "Early Stage Startup",
        "공공기관": "Public Sector",
        "비영리단체(NGO)": "NGO",
        "기타": "Other",
        "정보 없음": None
    }
    last_new_job_map = {
        "1년 전": "1",
        "2년 전": "2",
        "3년 전": "3",
        "4년 전": "4",
        "4년 이상": ">4",
        "이직 경험 없음": "never",
        "정보 없음": None
    }

    # -----------------------------
    # 입력 폼
    # -----------------------------
    with st.form("candidate_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎓 교육 및 경력")
            relevent_experience = st.selectbox("관련 경험 유무", list(relevent_experience_map.keys()))
            enrolled_university = st.selectbox("대학교 등록 상태", list(enrolled_university_map.keys()))
            education_level = st.selectbox("최종 학력", list(education_level_map.keys()))
            major_discipline = st.selectbox("전공 분야", list(major_discipline_map.keys()))

        with col2:
            st.subheader("🏢 직장 정보")
            experience = st.selectbox("총 경력 (년)", list(experience_map.keys()))
            company_size = st.selectbox("현재 회사 규모", list(company_size_map.keys()))
            company_type = st.selectbox("회사 유형", list(company_type_map.keys()))
            last_new_job = st.selectbox("마지막 이직 시기", list(last_new_job_map.keys()))

        st.divider()
        submitted = st.form_submit_button("🚀 합류 가능성 진단하기", use_container_width=True)

    # -----------------------------
    # 결과 표시
    # -----------------------------
    if submitted:
        # 한국어 → 영어 매핑 적용
        user_input = {
            "relevent_experience": relevent_experience_map[relevent_experience],
            "enrolled_university": enrolled_university_map[enrolled_university],
            "education_level": education_level_map[education_level],
            "major_discipline": major_discipline_map[major_discipline],
            "experience": experience_map[experience],
            "company_size": company_size_map[company_size],
            "company_type": company_type_map[company_type],
            "last_new_job": last_new_job_map[last_new_job]
        }

        with st.spinner("🔎 예측 중..."):
            try:
                prediction_prob = get_prediction(user_input)
                prediction_prob = float(prediction_prob) if prediction_prob else 0.0
                prediction_prob = max(0.0, min(1.0, prediction_prob))
            except Exception as e:
                st.error(f"예측 중 오류 발생: {e}")
                prediction_prob = 0.0

        # 결과 카드
        st.divider()
        st.subheader("📊 진단 결과")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("회사 합류 가능성", f"{prediction_prob:.1%}")
        with col2:
            if prediction_prob >= 0.6:
                join_level, icon = "높음", "🟢"
            elif prediction_prob >= 0.2:
                join_level, icon = "보통", "🟠"
            else:
                join_level, icon = "낮음", "🔴"
            st.metric("합류 가능성 수준", f"{icon} {join_level}")

        st.progress(prediction_prob)

        # 피드백 영역
        if prediction_prob < 0.1:
            st.error("❌ 아직 시작단계이지만, 당신과 비슷한 사람들도 성공한 사례도 있습니다. 많이 노력한다면 좋은 성과를 기대할 수 있습니다.")
        elif prediction_prob < 0.2:
            st.error("❌ 기본적인 토대가 마련되어 있으며, 꾸준한 노력이 좋은 성과로 이어질 수 있습니다.")
        elif prediction_prob < 0.3:
            st.warning("⚠️ 가능성을 보여주고 있으며, 조금 더 다듬으면 좋은 성과가 기대됩니다.")
        elif prediction_prob < 0.4:
            st.warning("⚠️ 안정적인 기반이 형성되고 있어, 발전의 여지가 큽니다.")
        elif prediction_prob < 0.5:
            st.warning("⚠️ 꾸준히 노력한 흔적이 보이며, 곧 긍정적인 변화를 만들 수 있습니다.")
        elif prediction_prob < 0.6:
            st.warning("⚠️ 대부분의 목표치에 근사하게 도달했으며, 곧 좋은 결과로 이어질 수 있습니다.")
        elif prediction_prob < 0.7:
            st.success("✅ 당신은 좋은 성장을 보여주고 있으며, 지속적인 성장가능성이 큽니다.")
        elif prediction_prob < 0.8:
            st.success("✅ 당신은 본사에서 필요한 기술에 대한 강점이 뚜렷하고 조금만 노력해도 더 높은 성과로 이어질 것으로 기대됩니다.")
        elif prediction_prob < 0.9:
            st.success("✅ 당신은 매우 우수한 지능을 가지고 있으며 기대이상의 결과가 가능합니다.")
        else:
            st.success("🌟 당신은 당사에서 원하는 완벽한 인재상입니다.")


        # 입력 정보 확인
        # with st.expander("📋 입력된 정보 (모델 입력값)"):
        #     st.dataframe(pd.DataFrame([user_input]), use_container_width=True)
