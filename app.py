import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Fitness Analyzer",
    page_icon="🏋️",
    layout="wide"
)

# ---- Custom CSS ----
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#141E30,#243B55);
}
.title {
    font-size:40px;
    text-align:center;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🏋️ AI Fitness Analyzer</div>", unsafe_allow_html=True)
st.write("### Your Personal AI Health Dashboard")

# ---- Sidebar Inputs ----
st.sidebar.header("Enter Your Details")

age = st.sidebar.number_input("Age", 10, 80, 21)
height = st.sidebar.number_input("Height (cm)", 100, 220)
weight = st.sidebar.number_input("Weight (kg)", 30, 150)

activity = st.sidebar.selectbox(
    "Activity Level",
    ["Low Activity","Moderate Activity","High Activity"]
)

goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["Weight Loss","Muscle Gain","Stay Fit"]
)

# ---- Analysis ----
if st.sidebar.button("Analyze Fitness"):

    bmi = weight / ((height/100)**2)

    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 25:
        status = "Healthy"
    elif bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    calories = int(weight * 24)

    col1, col2 = st.columns(2)

    # ---- Report ----
    with col1:
        st.subheader("🧠 AI Fitness Report")

        st.write(f"**Age:** {age}")
        st.write(f"**BMI:** {round(bmi,2)}")
        st.write(f"**Health Status:** {status}")
        st.write(f"**Daily Calories Needed:** {calories} kcal")

        st.subheader("🎯 Goal")
        st.write(goal)

        st.subheader("💪 Recommended Routine")
        st.write("• Cardio – 30 minutes daily")
        st.write("• Strength training – 3 days/week")
        st.write("• Hydration – 3L water")
        st.write("• Sleep – 7–8 hours")

    # ---- BMI Chart ----
    with col2:

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bmi,
            title={'text': "BMI Score"},
            gauge={
                'axis': {'range': [None,40]},
                'steps': [
                    {'range': [0,18.5], 'color': "lightblue"},
                    {'range': [18.5,25], 'color': "green"},
                    {'range': [25,30], 'color': "orange"},
                    {'range': [30,40], 'color': "red"}
                ]
            }
        ))

        st.plotly_chart(fig, use_container_width=True)