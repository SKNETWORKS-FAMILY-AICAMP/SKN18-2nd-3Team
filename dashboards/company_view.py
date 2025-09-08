import streamlit as st
import pandas as pd
import plotly.express as px

pd.set_option('future.no_silent_downcasting', True)

df = pd.read_csv("result_csv/result_test.csv")
df['experience'] = df['experience'].astype(str).str.strip()
experence_exp = df['experience'].replace({'<1':'0', '>20':'21'}).infer_objects(copy=False)
experence_exp = pd.to_numeric(experence_exp, errors='coerce')
experence_exp = experence_exp.dropna()
experence_exp = experence_exp.astype(int)
df = df.loc[experence_exp.index]
df['experience'] = experence_exp


def info_show():
        st.title("company view")

        important_columns = ["relevent_experience", "enrolled_university", "education_level", "major_discipline", "experience", "company_size", "company_type", "last_new_job", "prediction"]

        random_df = df[important_columns].copy() 


        random_df['prediction'] = random_df['prediction'].apply(
            lambda x: '🟢' 
            if x >= 0.6 else '🟡' 
            if x >= 0.2 else '🔴'
        )

        # prediction의 값이 🟢인 개수 count
        green_count = random_df[random_df['prediction'] == '🟢'].shape[0]
        yellow_count = random_df[random_df['prediction'] == '🟡'].shape[0]
        red_count = random_df[random_df['prediction'] == '🔴'].shape[0]
        # prediction값 비율
        green_pct = round((green_count / random_df.shape[0] * 100), 2)
        yellow_pct = round((yellow_count / random_df.shape[0] * 100), 2)
        red_pct = round((red_count / random_df.shape[0] * 100), 2)
        
        # 2행3열로 만들기
        st.subheader("Signal")
        info_df = pd.DataFrame({
            # 'Category': ['🟢', '🟡', '🔴'],
            'count(명)': [green_count, yellow_count, red_count],
            'percentage(%)': [green_pct, yellow_pct, red_pct]
        }).T

        # info_df = pd.DataFrame(info_df.to_numpy())
        info_df.columns = ['🟢(60%이상)', '🟡(20%이상 - 60% 미만)', '🔴(20%미만)']
        st.dataframe(info_df, use_container_width=True)

#-------------------------------------------------------------------------------------------------------------------------------------
def show():

    important_columns = ["relevent_experience", "enrolled_university", "education_level", "major_discipline", "experience", "company_size", "company_type", "last_new_job", "prediction"]

    random_df = df[important_columns] # 중요 컬럼 몇개만 뽑아서 

    random_df = df[important_columns].rename(columns={"prediction": "signal"})

    random_df['signal'] = random_df['signal'].apply(
        lambda x: '🟢' 
        if x >= 0.6 else '🟡' 
        if x >= 0.2 else '🔴'
    )
    st.dataframe(random_df, use_container_width=True)

#-------------------------------------------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

def graph1_show():
    prep_df = df[df['company_size'].isna() & df['company_type'].isna() & (df['last_new_job'] == 'never')]
    change_df = df[df['company_size'].isna() & df['company_type'].isna() & (df['last_new_job'] != 'never') & (df['last_new_job'] != 'nan')]
    worker_df = df[df['company_size'].notna() | df['company_type'].notna() | ((df['last_new_job'] != 'never') & (df['last_new_job'] != 'nan'))]

    def make_pie(data, title):
        green_count = data[data['prediction'] >= 0.6].shape[0]
        yellow_count = data[(data['prediction'] >= 0.2) & (data['prediction'] < 0.6)].shape[0]
        red_count = data[data['prediction'] < 0.2].shape[0]

        chart_data = pd.DataFrame({
            'Category': ['🟢', '🟡', '🔴'],
            'count': [green_count, yellow_count, red_count]
        })
        fig = px.pie(
            chart_data,
            values='count',
            names='Category',
            color='Category',
            title=title,
            color_discrete_map={
                '🟢': '#2ecc71',
                '🟡': '#ffd35c',
                '🔴': '#ff5c5c'
            }
        )
        return fig

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(make_pie(prep_df, "취업 경력이 없는 취업준비생"), use_container_width=True)

    with col2:
        st.plotly_chart(make_pie(change_df, "취업 경력이 있는 이직준비생"), use_container_width=True)

    with col3:
        st.plotly_chart(make_pie(worker_df, "현직자"), use_container_width=True)


#-------------------------------------------------------------------------------------------------------------------------------------
def graph2_show():
    st.title("지원자의 학력 & 재학 상태")

    # -------- 학력 파이차트 --------
    level_df = df['education_level'].value_counts()

    chart_data_level = pd.DataFrame({
        'Category': level_df.index.tolist(),
        'count': level_df.values.tolist()
    })

    fig_level = px.pie(
        chart_data_level, 
        values='count', 
        names='Category', 
        color='Category',
        color_discrete_map={
            'Graduate': 'red',
            'Masters': 'green', 
            'High School': 'blue',
            'Phd': 'pink',
            'Primary School': 'gray'
        }
    )

    # 학력별 🔴🟡🟢 비율 계산
    education_details = {}
    for level in level_df.index:
        level_data = df[df['education_level'] == level]
        green_count = level_data[level_data['prediction'] >= 0.6].shape[0]
        yellow_count = level_data[(level_data['prediction'] >= 0.2) & (level_data['prediction'] < 0.6)].shape[0]
        red_count = level_data[level_data['prediction'] < 0.2].shape[0]
        
        education_details[level] = {
            'green': green_count,
            'yellow': yellow_count,
            'red': red_count,
            'total': len(level_data)
        }

    custom_hover_level = []
    for level in chart_data_level['Category']:
        details = education_details[level]
        green_pct = (details['green']/details['total']*100) if details['total'] else 0
        yellow_pct = (details['yellow']/details['total']*100) if details['total'] else 0
        red_pct = (details['red']/details['total']*100) if details['total'] else 0
        hover_text = (
            f"<b>{level}</b><br>"
            f"Green: {green_pct:.2f}%<br>"
            f"Yellow: {yellow_pct:.2f}%<br>"
            f"Red: {red_pct:.2f}%<br>"
            "<extra></extra>"
        )
        custom_hover_level.append(hover_text)
    fig_level.data[0].hovertemplate = custom_hover_level


    # -------- 재학 상태 파이차트 --------
    enrolled_df = df['enrolled_university'].value_counts()

    chart_data_enrolled = pd.DataFrame({
        'Category': enrolled_df.index.tolist(),
        'count': enrolled_df.values.tolist()
    })

    fig_enrolled = px.pie(
        chart_data_enrolled, 
        values='count', 
        names='Category',
        color='Category',
        color_discrete_map={
            'no_enrollment': 'red',
            'Full time course': 'green', 
            'Part time course': 'blue'
        }
    )

    enrolled_details = {}
    for enrolled in enrolled_df.index:
        enrolled_data = df[df['enrolled_university'] == enrolled]
        green_count = enrolled_data[enrolled_data['prediction'] >= 0.6].shape[0]
        yellow_count = enrolled_data[(enrolled_data['prediction'] >= 0.2) & (enrolled_data['prediction'] < 0.6)].shape[0]
        red_count = enrolled_data[enrolled_data['prediction'] < 0.2].shape[0]
        
        enrolled_details[enrolled] = {
            'green': green_count,
            'yellow': yellow_count,
            'red': red_count,
            'total': len(enrolled_data)
        }

    custom_hover_enrolled = []
    for enrolled in chart_data_enrolled['Category']:
        details = enrolled_details[enrolled]
        green_pct = (details['green']/details['total']*100) if details['total'] else 0
        yellow_pct = (details['yellow']/details['total']*100) if details['total'] else 0
        red_pct = (details['red']/details['total']*100) if details['total'] else 0
        hover_text = (
            f"<b>{enrolled}</b><br>"
            f"Green: {green_pct:.2f}%<br>"
            f"Yellow: {yellow_pct:.2f}%<br>"
            f"Red: {red_pct:.2f}%<br>"
            "<extra></extra>"
        )
        custom_hover_enrolled.append(hover_text)
    fig_enrolled.data[0].hovertemplate = custom_hover_enrolled


    # -------- 한 줄에 배치 --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("지원자의 학력")
        st.plotly_chart(fig_level, use_container_width=True)

    with col2:
        st.subheader("지원자의 재학 상태")
        st.plotly_chart(fig_enrolled, use_container_width=True)

#-------------------------------------------------------------------------------------------------------------------------------------
def graph3_show():
    st.title("지원자의 전공")

    # --- 전공 파이차트 ---
    major_df = df['major_discipline'].value_counts()
    chart_data_major = pd.DataFrame({
        'Category': major_df.index.tolist(),
        'count': major_df.values.tolist()
    })

    fig_major = px.pie(
        chart_data_major, 
        values='count', 
        names='Category', 
        color='Category',
        color_discrete_map={
            'STEM': 'red',
            'Business Degree': 'green',
            'Arts': 'blue',
            'Other': 'gray',
            'No Major': 'pink',
            'other': 'purple'
        }
    )

    # --- 전공별 비율 계산 ---
    major_details = {}
    for major in major_df.index:
        major_data = df[df['major_discipline'] == major]
        green_count = major_data[major_data['prediction'] >= 0.6].shape[0]
        yellow_count = major_data[(major_data['prediction'] >= 0.2) & (major_data['prediction'] < 0.6)].shape[0]
        red_count = major_data[major_data['prediction'] < 0.2].shape[0]

        green_pct = round((green_count / major_data.shape[0] * 100), 2) if major_data.shape[0] > 0 else 0
        yellow_pct = round((yellow_count / major_data.shape[0] * 100), 2) if major_data.shape[0] > 0 else 0
        red_pct = round((red_count / major_data.shape[0] * 100), 2) if major_data.shape[0] > 0 else 0

        major_details[major] = {
            'green': green_pct,
            'yellow': yellow_pct,
            'red': red_pct,
        }

    major_dataframe = pd.DataFrame(major_details).T
    major_dataframe.columns = ['Green(%)', 'Yellow(%)', 'Red(%)']
    major_dataframe = major_dataframe.map(lambda x: f"{x:.2f}")

    # --- 한 줄에 배치 ---
    col1, col2 = st.columns([1.5, 1])  
    with col1:
        st.plotly_chart(fig_major, use_container_width=True)
    with col2:
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st.dataframe(major_dataframe, use_container_width=True)

    # --- 지원자의 연차 라인 차트 ---
    st.title("지원자의 연차")
    experience_df = df['experience'].value_counts()

    experience_details = {}
    for experience in experience_df.index:
        experience_data = df[df['experience'] == experience]
        green_count = experience_data[experience_data['prediction'] >= 0.6].shape[0]
        yellow_count = experience_data[(experience_data['prediction'] >= 0.2) & (experience_data['prediction'] < 0.6)].shape[0]
        red_count = experience_data[experience_data['prediction'] < 0.2].shape[0]

        experience_details[experience] = {
            'green': green_count,
            'yellow': yellow_count,
            'red': red_count,
        }

    experience_dataframe = pd.DataFrame(experience_details).T
    experience_dataframe = experience_dataframe.sort_index()

    fig_line = px.line(
        experience_dataframe.reset_index(),
        x="index", 
        y=["green", "yellow", "red"],
        labels={"index": "경력", "value": "지원자 수", "variable": "합류 비율"},
        color_discrete_map={
            "green": "#2ecc71",
            "yellow": "#ffd35c",
            "red": "#ff5c5c"
        }
    )

    st.plotly_chart(fig_line, use_container_width=True)