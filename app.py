import streamlit as st
import random
import pandas as pd
import database as db
from auth import create_jwt, verify_jwt, send_otp_via_sendgrid
import model

# -----------------------
# INITIALIZE DATABASE
# -----------------------
db.init_db()

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="FitPlan AI",
    page_icon="💪",
    layout="wide"
)

# -----------------------
# SESSION STATES
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# =====================================================
# LOGIN PAGE
# =====================================================
if st.session_state.page == "login":

    st.title("💪 FitPlan AI - Personalized Fitness Planner")

    login_method = st.radio("Login via", ["Password", "OTP"])

    email = st.text_input("Email")

    if login_method == "Password":

        password = st.text_input("Password", type="password")

        if st.button("LOGIN"):

            user = db.verify_user(email, password)

            if user:
                st.session_state.user_email = email
                st.session_state.token = create_jwt(email)
                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error("Invalid email or password")

    else:

        if st.button("Generate OTP"):

            otp = str(random.randint(100000, 999999))
            st.session_state.generated_otp = otp

            if send_otp_via_sendgrid(email, otp):
                st.success("OTP sent successfully")

        user_otp = st.text_input("Enter OTP")

        if st.button("Verify OTP"):

            if user_otp == st.session_state.generated_otp:
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error("Invalid OTP")

    st.divider()

    if st.button("Create New Account"):
        st.session_state.page = "signup"
        st.rerun()


# =====================================================
# SIGNUP PAGE
# =====================================================
elif st.session_state.page == "signup":

    st.title("Create Account")

    name = st.text_input("Full Name")
    age = st.number_input("Age", 10, 80)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    goal = st.selectbox(
        "Fitness Goal",
        ["Build Muscle", "Lose Weight", "Improve Cardio", "Flexibility"]
    )

    if st.button("Register"):

        result = db.add_user(name, age, gender, email, password, goal)

        if result:
            st.success("Account Created Successfully")
            st.session_state.page = "login"
            st.rerun()

        else:
            st.error("Email already exists")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# =====================================================
# DASHBOARD
# =====================================================
elif st.session_state.page == "dashboard":

    if "token" not in st.session_state:
        st.session_state.page = "login"
        st.rerun()

    st.title("🏋️ FitPlan AI Dashboard")

    st.subheader("Personal Details")

    name = st.text_input("Name")
    age = st.number_input("Age", 10, 80)
    height = st.number_input("Height (cm)", 100, 220)
    weight = st.number_input("Weight (kg)", 30, 200)

    st.subheader("Fitness Details")

    goal = st.selectbox(
        "Goal",
        ["Build Muscle", "Lose Weight", "Improve Cardio", "Flexibility"]
    )

    equipment = st.selectbox(
        "Equipment",
        ["No Equipment", "Dumbbells", "Gym Equipment"]
    )

    level = st.selectbox(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("Generate AI Workout Plan"):

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 2)

        bmi_status = "Normal"

        if bmi > 25:
            bmi_status = "Overweight"

        ai_response = model.generate_workout(
            name, age, goal, level, equipment, bmi_status
        )

        st.session_state.generated_plan = ai_response
        st.session_state.user_details = {"name": name, "goal": goal}

        db.save_workout(st.session_state.user_email, goal, ai_response)

        st.session_state.page = "view_plan"
        st.rerun()

    st.markdown("---")

    if st.button("📊 Weight Tracker"):
        st.session_state.page = "weight_tracker"
        st.rerun()

    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()


# =====================================================
# VIEW PLAN PAGE
# =====================================================
elif st.session_state.page == "view_plan":

    st.title("🔥 Your Personalized Workout Plan")

    st.subheader(f"Plan for {st.session_state.user_details['name']}")

    st.info(st.session_state.generated_plan)

    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()


# =====================================================
# WEIGHT TRACKER PAGE
# =====================================================
elif st.session_state.page == "weight_tracker":

    st.title("⚖ Weight Tracker")

    email = st.session_state.user_email

    st.subheader("Enter today's weight")

    weight = st.number_input("Weight (kg)", 30.0, 200.0)

    if st.button("Save Weight"):

        db.save_weight(email, weight)

        st.success("Weight saved successfully!")

        st.rerun()

    st.markdown("---")

    st.subheader("Weight History")

    history = db.get_weight_history(email)

    if history:

        df = pd.DataFrame(history, columns=["Weight", "Date"])

        st.dataframe(df)

        st.subheader("Weight Progress")

        st.line_chart(df["Weight"])

    else:
        st.info("No weight records found")

    st.markdown("---")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()