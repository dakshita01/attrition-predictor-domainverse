import streamlit as st
import pandas as pd
import joblib
import plotly.express as px


st.set_page_config(
    page_title="Employee Attrition Risk Predictor",
    page_icon=None,
    layout="wide"
)


# Custom styling

st.markdown("""
<style>

:root {
    --purple-light: #D7B0D5;
    --purple-mid-light: #B08DCA;
    --purple-mid: #7E64AD;
    --purple-dark: #1E1D4B;

    --bg-light: #D7B0D5;
    --bg-mid-light: #C8A2CF;
    --bg-mid: #B08DCA;
    --bg-dark: #7E64AD;

    --input-bg: #F5EAF5;
    --border: #B08DCA;
}


/* Main background */

.stApp {
    background: linear-gradient(
        180deg,
        #D7B0D5 0%,
        #C8A2CF 35%,
        #B08DCA 68%,
        #7E64AD 100%
    );

    color: var(--purple-dark);
}


.block-container {
    max-width: 1400px;
    padding-top: 2.5rem;
    padding-bottom: 5rem;
}


/* Title */

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 750;
    color: var(--purple-dark);
    letter-spacing: -1px;
    margin-bottom: 0.4rem;
}

.title-highlight {
    color: var(--purple-mid);
}

.main-subtitle {
    text-align: center;
    color: var(--purple-dark);
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
}

.top-line {
    width: 70px;
    height: 4px;
    background: var(--purple-dark);
    border-radius: 10px;
    margin: 0 auto 1.2rem auto;
}


/* Introduction */

.intro-box {
    max-width: 950px;
    margin: 1.7rem auto 0.8rem auto;
    text-align: center;
    background: transparent;
    border: none;
    box-shadow: none;
    padding: 0;
}

.intro-title {
    color: var(--purple-dark);
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.65rem;
}

.intro-text {
    color: var(--purple-dark);
    font-size: 0.98rem;
    line-height: 1.7;
}


/* Typing text */

.quote-container {
    position: relative;
    height: 35px;
    max-width: 900px;
    margin: 1.1rem auto 1.7rem auto;
    text-align: center;
    overflow: hidden;
}

.quote {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;

    opacity: 0;
    overflow: hidden;
    white-space: nowrap;

    color: var(--purple-dark);
    font-size: 1rem;
    font-style: italic;

    width: 0;
    margin: auto;

    border: none !important;
}


.quote-one {
    animation: quoteOne 18s infinite;
}

.quote-two {
    animation: quoteTwo 18s infinite;
}

.quote-three {
    animation: quoteThree 18s infinite;
}


@keyframes quoteOne {

    0% {
        opacity: 0;
        width: 0;
    }

    5% {
        opacity: 1;
        width: 0;
    }

    18% {
        opacity: 1;
        width: 100%;
    }

    28% {
        opacity: 0;
        width: 100%;
    }

    100% {
        opacity: 0;
        width: 100%;
    }
}


@keyframes quoteTwo {

    0% {
        opacity: 0;
        width: 0;
    }

    32% {
        opacity: 0;
        width: 0;
    }

    37% {
        opacity: 1;
        width: 0;
    }

    50% {
        opacity: 1;
        width: 100%;
    }

    60% {
        opacity: 0;
        width: 100%;
    }

    100% {
        opacity: 0;
        width: 100%;
    }
}


@keyframes quoteThree {

    0% {
        opacity: 0;
        width: 0;
    }

    64% {
        opacity: 0;
        width: 0;
    }

    69% {
        opacity: 1;
        width: 0;
    }

    82% {
        opacity: 1;
        width: 100%;
    }

    92% {
        opacity: 0;
        width: 100%;
    }

    100% {
        opacity: 0;
        width: 100%;
    }
}


/* Start button */

.start-button-container {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0 auto 2rem auto !important;
}

.start-button-container button {
    width: 230px !important;
    background-color: var(--purple-mid) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
    padding: 0.7rem 1.5rem !important;
    box-shadow: 0 6px 18px rgba(30, 29, 75, 0.18);
}

.start-button-container button:hover {
    background-color: var(--purple-dark) !important;
    color: #FFFFFF !important;
}


/* Section headings */

.section-title {
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--purple-dark);
    margin-top: 1.8rem;
    margin-bottom: 1.3rem;
    padding-bottom: 0.55rem;
    border-bottom: 2px solid rgba(30, 29, 75, 0.28);
}

.job-section {
    margin-top: 3.5rem;
}


/* Input labels */

.stNumberInput label,
.stSelectbox label {
    color: var(--purple-dark) !important;
    font-weight: 600 !important;
}


/* Number inputs */

.stNumberInput > div > div {
    background-color: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 11px !important;
    box-shadow: none !important;
}

.stNumberInput input {
    color: var(--purple-dark) !important;
    background-color: transparent !important;
}


/* Plus / minus */

.stNumberInput button {
    background: transparent !important;
    color: var(--purple-dark) !important;
    border: none !important;
    border-left: none !important;
    border-right: none !important;
    box-shadow: none !important;
    width: 30px !important;
    min-width: 30px !important;
    padding: 0 !important;
}

.stNumberInput button:hover {
    background: transparent !important;
    color: var(--purple-mid) !important;
    border: none !important;
    box-shadow: none !important;
}

.stNumberInput button svg {
    fill: var(--purple-dark) !important;
    color: var(--purple-dark) !important;
}

.stNumberInput button:hover svg {
    fill: var(--purple-mid) !important;
    color: var(--purple-mid) !important;
}

.stNumberInput [data-baseweb="input"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}


/* Select boxes */

.stSelectbox > div > div {
    background-color: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 11px !important;
    box-shadow: none !important;
}

.stSelectbox input {
    color: var(--purple-dark) !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: var(--purple-dark) !important;
}


/* Prediction button */

.stButton > button {
    background-color: var(--purple-mid) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
    padding: 0.7rem 1rem !important;
    margin-top: 1.5rem;
    box-shadow: 0 6px 18px rgba(30, 29, 75, 0.18);
}

.stButton > button:hover {
    background-color: var(--purple-dark) !important;
    color: #FFFFFF !important;
}


/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid rgba(30, 29, 75, 0.28);
}

.stTabs [data-baseweb="tab"] {
    color: var(--purple-dark) !important;
    font-weight: 650 !important;
    padding: 0.7rem 1.2rem;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"] p {
    color: var(--purple-dark) !important;
    font-weight: 650 !important;
}

.stTabs [aria-selected="true"] {
    color: var(--purple-dark) !important;
    border-bottom: 3px solid var(--purple-dark) !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] p {
    color: var(--purple-dark) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--purple-mid) !important;
}

.stTabs [data-baseweb="tab"]:hover p {
    color: var(--purple-mid) !important;
}


/* Metric cards */

[data-testid="stMetric"] {
    background: rgba(245, 234, 245, 0.82);
    border: 1px solid rgba(126, 100, 173, 0.30);
    border-radius: 14px;
    padding: 1rem;
    box-shadow: 0 6px 20px rgba(30, 29, 75, 0.08);
}

[data-testid="stMetricLabel"] {
    color: var(--purple-dark) !important;
}

[data-testid="stMetricValue"] {
    color: var(--purple-dark) !important;
}


/* Charts */

[data-testid="stPlotlyChart"] {
    background: rgba(245, 234, 245, 0.78);
    border-radius: 14px;
    border: 1px solid rgba(126, 100, 173, 0.25);
    padding: 0.4rem;
}


/* Dividers */

hr {
    border: none;
    border-top: 1px solid rgba(30, 29, 75, 0.22);
    margin: 2rem 0;
}


/* Progress bar */

.stProgress > div > div > div > div {
    background-color: var(--purple-mid) !important;
}


/* Caption */

.stCaption {
    color: var(--purple-dark) !important;
}


/* Alerts */

[data-testid="stAlert"] {
    color: var(--purple-dark) !important;
}


/* General text */

.stMarkdown,
.stText,
p,
label {
    color: var(--purple-dark);
}

</style>
""", unsafe_allow_html=True)


# Load saved model files

@st.cache_resource
def load_artifacts():

    model = joblib.load(
        "outputs/attrition_model.pkl"
    )

    scaler = joblib.load(
        "outputs/scaler.pkl"
    )

    model_columns = joblib.load(
        "outputs/model_columns.pkl"
    )

    return model, scaler, model_columns


@st.cache_data
def load_data():

    return pd.read_csv(
        "data/employee_attrition.csv"
    )


model, scaler, model_columns = load_artifacts()

df = load_data()


# Risk classification

def get_risk_level(probability):

    if probability < 0.33:
        return "Low"

    elif probability < 0.66:
        return "Medium"

    else:
        return "High"


# Title

st.markdown(
    '<div class="top-line"></div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">'
    'Employee <span class="title-highlight">Attrition</span> Risk Predictor'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-subtitle">'
    'Predictive analytics for understanding employee attrition risk'
    '</div>',
    unsafe_allow_html=True
)


# Session state

if "show_prediction" not in st.session_state:

    st.session_state.show_prediction = False


# Introduction screen

if not st.session_state.show_prediction:

    st.markdown(
        '<div class="intro-box">'
        '<div class="intro-title">'
        'Understand. Predict. Act.'
        '</div>'

        '<div class="intro-text">'
        'This application uses employee information such as job satisfaction, '
        'income, experience, overtime, workplace factors and job details '
        'to estimate the probability of employee attrition.'
        '<br>'
        'The prediction is generated using a trained Logistic Regression '
        'model and presented as a Low, Medium or High risk level.'
        '</div>'

        '</div>',
        unsafe_allow_html=True
    )


    # Typing quotes

    st.markdown(
        '<div class="quote-container">'

        '<div class="quote quote-one">'
        '"Data turns employee patterns into actionable insights."'
        '</div>'

        '<div class="quote quote-two">'
        '"Understanding risk is the first step toward better decisions."'
        '</div>'

        '<div class="quote quote-three">'
        '"Predictive analytics helps organizations act before problems grow."'
        '</div>'

        '</div>',
        unsafe_allow_html=True
    )


    # Start Prediction button

    start_col1, start_col2, start_col3 = st.columns(
        [1, 1, 1]
    )


    with start_col2:

        st.markdown(
            '<div class="start-button-container">',
            unsafe_allow_html=True
        )

        if st.button(
            "Start Prediction",
            use_container_width=True
        ):

            st.session_state.show_prediction = True

            st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    st.stop()


# Prediction and Dashboard

tab1, tab2 = st.tabs(
    [
        "Predict Risk",
        "Insights Dashboard"
    ]
)


# Prediction tab

with tab1:

    st.markdown(
        '<div class="section-title">'
        'Employee Details'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    # Column 1

    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=60,
            value=30,
            step=1
        )

        daily_rate = st.number_input(
            "Daily Rate",
            min_value=100,
            max_value=1500,
            value=800,
            step=10
        )

        distance = st.number_input(
            "Distance From Home",
            min_value=1,
            max_value=30,
            value=5,
            step=1
        )

        education = st.number_input(
            "Education Level",
            min_value=1,
            max_value=5,
            value=3,
            step=1
        )

        environment_satisfaction = st.number_input(
            "Environment Satisfaction",
            min_value=1,
            max_value=4,
            value=3,
            step=1
        )

        hourly_rate = st.number_input(
            "Hourly Rate",
            min_value=30,
            max_value=100,
            value=65,
            step=1
        )

        job_involvement = st.number_input(
            "Job Involvement",
            min_value=1,
            max_value=4,
            value=3,
            step=1
        )


    # Column 2

    with col2:

        job_level = st.number_input(
            "Job Level",
            min_value=1,
            max_value=5,
            value=2,
            step=1
        )

        job_satisfaction = st.number_input(
            "Job Satisfaction",
            min_value=1,
            max_value=4,
            value=3,
            step=1
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=1000,
            max_value=20000,
            value=5000,
            step=500
        )

        monthly_rate = st.number_input(
            "Monthly Rate",
            min_value=2000,
            max_value=27000,
            value=14000,
            step=500
        )

        num_companies = st.number_input(
            "Number of Companies Worked",
            min_value=0,
            max_value=10,
            value=2,
            step=1
        )

        salary_hike = st.number_input(
            "Percent Salary Hike",
            min_value=10,
            max_value=25,
            value=15,
            step=1
        )

        performance_rating = st.number_input(
            "Performance Rating",
            min_value=1,
            max_value=5,
            value=3,
            step=1
        )


    # Column 3

    with col3:

        relationship_satisfaction = st.number_input(
            "Relationship Satisfaction",
            min_value=1,
            max_value=4,
            value=3,
            step=1
        )

        stock_option = st.number_input(
            "Stock Option Level",
            min_value=0,
            max_value=3,
            value=1,
            step=1
        )

        total_working_years = st.number_input(
            "Total Working Years",
            min_value=0,
            max_value=40,
            value=8,
            step=1
        )

        training_times = st.number_input(
            "Training Times Last Year",
            min_value=0,
            max_value=10,
            value=3,
            step=1
        )

        worklife = st.number_input(
            "Work Life Balance",
            min_value=1,
            max_value=4,
            value=3,
            step=1
        )

        years_company = st.number_input(
            "Years At Company",
            min_value=0,
            max_value=40,
            value=5,
            step=1
        )

        years_current_role = st.number_input(
            "Years In Current Role",
            min_value=0,
            max_value=18,
            value=3,
            step=1
        )


    # Remaining employee details

    col1, col2 = st.columns(2)


    with col1:

        years_promotion = st.number_input(
            "Years Since Last Promotion",
            min_value=0,
            max_value=15,
            value=1,
            step=1
        )


    with col2:

        years_manager = st.number_input(
            "Years With Current Manager",
            min_value=0,
            max_value=17,
            value=3,
            step=1
        )


    # Job Information

    st.markdown(
        '<div class="job-section"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">'
        'Job Information'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        overtime = st.selectbox(
            "OverTime",
            sorted(
                df["OverTime"].unique()
            )
        )

        business_travel = st.selectbox(
            "Business Travel",
            sorted(
                df["BusinessTravel"].unique()
            )
        )

        marital_status = st.selectbox(
            "Marital Status",
            sorted(
                df["MaritalStatus"].unique()
            )
        )


    with col2:

        department = st.selectbox(
            "Department",
            sorted(
                df["Department"].unique()
            )
        )

        education_field = st.selectbox(
            "Education Field",
            sorted(
                df["EducationField"].unique()
            )
        )


    with col3:

        job_role = st.selectbox(
            "Job Role",
            sorted(
                df["JobRole"].unique()
            )
        )

        gender = st.selectbox(
            "Gender",
            sorted(
                df["Gender"].unique()
            )
        )


    # Prediction

    if st.button(
        "Predict Attrition Risk",
        type="primary",
        use_container_width=True
    ):

        input_dict = {

            "Age": age,

            "DailyRate": daily_rate,

            "DistanceFromHome": distance,

            "Education": education,

            "EnvironmentSatisfaction":
                environment_satisfaction,

            "HourlyRate": hourly_rate,

            "JobInvolvement": job_involvement,

            "JobLevel": job_level,

            "JobSatisfaction":
                job_satisfaction,

            "MonthlyIncome": monthly_income,

            "MonthlyRate": monthly_rate,

            "NumCompaniesWorked":
                num_companies,

            "PercentSalaryHike":
                salary_hike,

            "PerformanceRating":
                performance_rating,

            "RelationshipSatisfaction":
                relationship_satisfaction,

            "StockOptionLevel":
                stock_option,

            "TotalWorkingYears":
                total_working_years,

            "TrainingTimesLastYear":
                training_times,

            "WorkLifeBalance":
                worklife,

            "YearsAtCompany":
                years_company,

            "YearsInCurrentRole":
                years_current_role,

            "YearsSinceLastPromotion":
                years_promotion,

            "YearsWithCurrManager":
                years_manager,

            "BusinessTravel":
                business_travel,

            "Department":
                department,

            "EducationField":
                education_field,

            "Gender":
                gender,

            "JobRole":
                job_role,

            "MaritalStatus":
                marital_status,

            "OverTime":
                overtime
        }


        input_df = pd.DataFrame(
            [input_dict]
        )


        categorical_cols = (
            input_df
            .select_dtypes(
                include="object"
            )
            .columns
            .tolist()
        )


        input_encoded = pd.get_dummies(
            input_df,
            columns=categorical_cols,
            drop_first=True
        )


        input_encoded = input_encoded.reindex(
            columns=model_columns,
            fill_value=0
        )


        input_scaled = scaler.transform(
            input_encoded
        )


        probability = model.predict_proba(
            input_scaled
        )[0][1]


        risk = get_risk_level(
            probability
        )


        # Prediction result

        st.divider()


        st.markdown(
            '<div class="section-title">'
            'Prediction Result'
            '</div>',
            unsafe_allow_html=True
        )


        result_col1, result_col2 = st.columns(2)


        with result_col1:

            st.metric(
                "Attrition Probability",
                f"{probability * 100:.1f}%"
            )


        with result_col2:

            if risk == "Low":

                st.success(
                    f"Risk Level: {risk}"
                )

            elif risk == "Medium":

                st.warning(
                    f"Risk Level: {risk}"
                )

            else:

                st.error(
                    f"Risk Level: {risk}"
                )


        st.progress(
            min(
                int(probability * 100),
                100
            )
        )


        st.caption(
            "Low: <33% | Medium: 33%-<66% | High: >=66%"
        )


        st.caption(
            "The prediction represents model-estimated risk "
            "and should be interpreted as a data-driven indicator "
            "rather than a certainty."
        )


# Insights dashboard

with tab2:

    st.markdown(
        '<div class="section-title">'
        'Insights Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


    total_employees = len(df)


    employees_left = (
        df["Attrition"] == "Yes"
    ).sum()


    attrition_rate = (
        employees_left / total_employees
    ) * 100


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Employees",
        total_employees
    )


    col2.metric(
        "Employees Left",
        employees_left
    )


    col3.metric(
        "Attrition Rate",
        f"{attrition_rate:.1f}%"
    )


    st.divider()


    col1, col2 = st.columns(2)


    # Department chart

    with col1:

        fig1 = px.histogram(
            df,
            x="Department",
            color="Attrition",
            barmode="group",
            title="Attrition by Department",
            color_discrete_sequence=[
                "#7E64AD",
                "#B08DCA"
            ]
        )


        fig1.update_layout(
            plot_bgcolor="rgba(245,234,245,0.78)",
            paper_bgcolor="rgba(245,234,245,0.78)",

            font=dict(
                color="#1E1D4B"
            ),

            title_font=dict(
                color="#1E1D4B",
                size=18
            ),

            xaxis=dict(
                title_font=dict(
                    color="#1E1D4B"
                ),
                tickfont=dict(
                    color="#1E1D4B"
                ),
                gridcolor="rgba(30,29,75,0.12)"
            ),

            yaxis=dict(
                title_font=dict(
                    color="#1E1D4B"
                ),
                tickfont=dict(
                    color="#1E1D4B"
                ),
                gridcolor="rgba(30,29,75,0.12)"
            ),

            legend=dict(
                font=dict(
                    color="#1E1D4B"
                )
            )
        )


        st.plotly_chart(
            fig1,
            use_container_width=True
        )


    # Overtime chart

    with col2:

        fig2 = px.histogram(
            df,
            x="OverTime",
            color="Attrition",
            barmode="group",
            title="Attrition by Overtime",
            color_discrete_sequence=[
                "#7E64AD",
                "#B08DCA"
            ]
        )


        fig2.update_layout(
            plot_bgcolor="rgba(245,234,245,0.78)",
            paper_bgcolor="rgba(245,234,245,0.78)",

            font=dict(
                color="#1E1D4B"
            ),

            title_font=dict(
                color="#1E1D4B",
                size=18
            ),

            xaxis=dict(
                title_font=dict(
                    color="#1E1D4B"
                ),
                tickfont=dict(
                    color="#1E1D4B"
                ),
                gridcolor="rgba(30,29,75,0.12)"
            ),

            yaxis=dict(
                title_font=dict(
                    color="#1E1D4B"
                ),
                tickfont=dict(
                    color="#1E1D4B"
                ),
                gridcolor="rgba(30,29,75,0.12)"
            ),

            legend=dict(
                font=dict(
                    color="#1E1D4B"
                )
            )
        )


        st.plotly_chart(
            fig2,
            use_container_width=True
        )


    # Income chart

    fig3 = px.box(
        df,
        x="Attrition",
        y="MonthlyIncome",
        title="Monthly Income vs Attrition",
        color="Attrition",
        color_discrete_sequence=[
            "#7E64AD",
            "#B08DCA"
        ]
    )


    fig3.update_layout(
        plot_bgcolor="rgba(245,234,245,0.78)",
        paper_bgcolor="rgba(245,234,245,0.78)",

        font=dict(
            color="#1E1D4B"
        ),

        title_font=dict(
            color="#1E1D4B",
            size=18
        ),

        xaxis=dict(
            title_font=dict(
                color="#1E1D4B"
            ),
            tickfont=dict(
                color="#1E1D4B"
            ),
            gridcolor="rgba(30,29,75,0.12)"
        ),

        yaxis=dict(
            title_font=dict(
                color="#1E1D4B"
            ),
            tickfont=dict(
                color="#1E1D4B"
            ),
            gridcolor="rgba(30,29,75,0.12)"
        ),

        legend=dict(
            font=dict(
                color="#1E1D4B"
            )
        )
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    st.caption(
        "The dashboard shows patterns in the dataset "
        "and does not imply causation."
    )