import streamlit as st
import random
import database as db
from auth import create_jwt, send_otp_via_brevo
import model

# ---------------- DB INIT ----------------
db.init_db()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FitPlan AI", page_icon="💪", layout="wide")

# ---------------- SESSION STATES ----------------
defaults = {
    "page": "login",
    "generated_otp": None,
    "user_email": None,
    "name": "",
    "age": 20,
    "gender": "Male",
    "goal": "Build Muscle",
    "height": 170,
    "weight": 70
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ================= LOGIN PAGE =================
if st.session_state.page == "login":

    st.title("💪 FitPlan AI Login")

    login_type = st.radio("Login Method", ["Password", "OTP"])

    email = st.text_input("Email")

    # -------- PASSWORD LOGIN --------
    if login_type == "Password":

        password = st.text_input("Password", type="password")

        if st.button("Login"):

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
                st.error("Invalid credentials")

    # -------- OTP LOGIN --------
    else:

        if st.button("Generate OTP"):
            otp = str(random.randint(100000, 999999))
            st.session_state.generated_otp = otp
            send_otp_via_brevo(email, otp)
            st.success("OTP Sent")

        entered = st.text_input("Enter OTP")

        if st.button("Verify Login"):

            if entered == st.session_state.generated_otp:

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
                st.error("Wrong OTP")

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()


# ================= SIGNUP =================
elif st.session_state.page == "signup":

    st.title("Signup")

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

    st.title("🏋️ Dashboard")
    st.success(f"Welcome {st.session_state.name}")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Profile", "Workout", "Weight Tracker", "Logout"]
    )

    # -------- PROFILE --------
    with tab1:

        st.session_state.name = st.text_input(
            "Name",
            value=st.session_state.name
        )

        st.session_state.age = st.number_input(
            "Age",
            10, 80,
            value=st.session_state.age
        )

        st.session_state.height = st.number_input(
            "Height (cm)",
            100, 220,
            value=st.session_state.height
        )

        st.session_state.weight = st.number_input(
            "Weight (kg)",
            30, 200,
            value=st.session_state.weight
        )

        if st.button("Update Profile"):

            db.update_profile(
                st.session_state.name,
                st.session_state.age,
                st.session_state.gender,
                st.session_state.goal,
                st.session_state.user_email
            )

            st.success("Profile Saved")

    # -------- WORKOUT --------
    with tab2:

        goal = st.selectbox(
            "Goal",
            ["Build Muscle", "Lose Weight", "Cardio"]
        )

        equipment = st.selectbox(
            "Equipment",
            ["No Equipment", "Dumbbells", "Gym"]
        )

        level = st.selectbox(
            "Fitness Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        if st.button("Generate Workout"):

            height_m = st.session_state.height / 100
            bmi = round(
                st.session_state.weight / (height_m ** 2),
                2
            )

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

            st.success("Workout Generated")
            st.write(plan)

            db.save_workout(
                st.session_state.user_email,
                goal,
                plan
            )

    # -------- WEIGHT --------
    with tab3:

        w = st.number_input("Today's Weight", 30.0, 200.0)

        if st.button("Save Weight"):
            db.save_weight(
                st.session_state.user_email,
                w,
                "today"
            )
            st.success("Saved")

        history = db.get_weights(
            st.session_state.user_email
        )

        if history:
            st.line_chart(history)

    # -------- LOGOUT --------
    with tab4:

        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()