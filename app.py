import streamlit as st
import random
import database as db
from auth import create_jwt, send_otp_via_brevo
import model

# ---------------- INIT DB ----------------
db.init_db()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FitPlan AI", page_icon="💪", layout="wide")

# ---------------- SESSION STATES ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "name" not in st.session_state:
    st.session_state.name = ""

if "age" not in st.session_state:
    st.session_state.age = 20

if "gender" not in st.session_state:
    st.session_state.gender = "Male"

if "goal" not in st.session_state:
    st.session_state.goal = "Build Muscle"

if "height" not in st.session_state:
    st.session_state.height = 170

if "weight" not in st.session_state:
    st.session_state.weight = 70


# ================= LOGIN =================
if st.session_state.page == "login":

    st.title("💪 FitPlan AI Login")

    login_method = st.radio("Login via", ["Password", "OTP"])

    email = st.text_input("Email")

    if login_method == "Password":

        password = st.text_input("Password", type="password")

        if st.button("LOGIN"):

            user = db.verify_user(email, password)

            if user:

                st.session_state.user_email = email
                st.session_state.token = create_jwt(email)

                # ⭐ AUTO LOAD PROFILE
                profile = db.get_user_profile(email)

                if profile:
                    st.session_state.name = profile[0]
                    st.session_state.age = profile[1]
                    st.session_state.gender = profile[2]
                    st.session_state.goal = profile[3]

                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error("Invalid Login")

    else:

        if st.button("Generate OTP"):

            otp = str(random.randint(100000, 999999))
            st.session_state.generated_otp = otp

            if send_otp_via_brevo(email, otp):
                st.success("OTP Sent")

        user_otp = st.text_input("Enter OTP")

        if st.button("Verify & Login"):

            if user_otp == st.session_state.generated_otp:

                st.session_state.user_email = email
                st.session_state.token = create_jwt(email)

                profile = db.get_user_profile(email)

                if profile:
                    st.session_state.name = profile[0]
                    st.session_state.age = profile[1]
                    st.session_state.gender = profile[2]
                    st.session_state.goal = profile[3]

                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error("Invalid OTP")

    if st.button("Signup"):
        st.session_state.page = "signup"
        st.rerun()


# ================= SIGNUP =================
elif st.session_state.page == "signup":

    st.title("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", 10, 80)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    goal = st.selectbox("Goal", ["Build Muscle", "Lose Weight", "Improve Cardio"])

    if st.button("Register"):

        ok = db.add_user(name, age, gender, email, password, goal)

        if ok:
            st.success("Account Created")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("User already exists")

    if st.button("Back"):
        st.session_state.page = "login"
        st.rerun()


# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":

    st.title("🏋️ FitPlan Dashboard")
    st.info(f"Welcome {st.session_state.name}")

    tabs = st.tabs(["Profile", "Workout", "Weight", "Logout"])

    # ------- PROFILE -------
    with tabs[0]:

        st.session_state.name = st.text_input("Name", value=st.session_state.name)
        st.session_state.age = st.number_input("Age", 10, 80, value=st.session_state.age)
        st.session_state.height = st.number_input("Height", 100, 220, value=st.session_state.height)
        st.session_state.weight = st.number_input("Weight", 30, 200, value=st.session_state.weight)

        if st.button("Update Profile"):

            db.update_profile(
                st.session_state.name,
                st.session_state.age,
                st.session_state.gender,
                st.session_state.goal,
                st.session_state.user_email
            )

            st.success("Profile Updated")

    # ------- WORKOUT -------
    with tabs[1]:

        goal = st.selectbox("Goal", ["Build Muscle", "Lose Weight", "Cardio"])
        equipment = st.selectbox("Equipment", ["No Equipment", "Dumbbells", "Gym"])
        level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])

        if st.button("Generate Workout"):

            height_m = st.session_state.height / 100
            bmi = round(st.session_state.weight / (height_m ** 2), 2)

            bmi_status = "Normal"
            if bmi > 25:
                bmi_status = "Overweight"

            plan = model.generate_workout(
                st.session_state.name,
                st.session_state.age,
                goal,
                level,
                equipment,
                bmi_status
            )

            st.success("Plan Generated")
            st.write(plan)

            db.save_workout(st.session_state.user_email, goal, plan)

    # ------- WEIGHT -------
    with tabs[2]:

        w = st.number_input("Today's Weight", 30.0, 200.0)

        if st.button("Save Weight"):
            db.save_weight(st.session_state.user_email, w, "today")
            st.success("Saved")

        data = db.get_weights(st.session_state.user_email)

        if data:
            st.line_chart(data)

    # ------- LOGOUT -------
    with tabs[3]:

        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()