import streamlit as st
from database import create_user, verify_user
from auth import generate_otp, send_otp_via_sendgrid, create_jwt

st.set_page_config(page_title="FitPlan AI", page_icon="💪")

# -----------------------------
# SESSION STATES
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "otp" not in st.session_state:
    st.session_state.otp = None

if "email" not in st.session_state:
    st.session_state.email = None

# -----------------------------
# LOGIN PAGE
# -----------------------------
if st.session_state.page == "login":

    st.title("💪 FitPlan AI Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = verify_user(email, password)

        if user:

            otp = generate_otp()

            sent = send_otp_via_sendgrid(email, otp)

            if sent:

                st.session_state.otp = otp
                st.session_state.email = email
                st.session_state.page = "otp"

                st.success("OTP sent to your email")
                st.rerun()

            else:
                st.error("Failed to send OTP")

        else:
            st.error("Invalid email or password")

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

# -----------------------------
# SIGNUP PAGE
# -----------------------------
elif st.session_state.page == "signup":

    st.title("Create Account")

    name = st.text_input("Full Name")
    age = st.number_input("Age", 10, 80)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    goal = st.selectbox(
        "Fitness Goal",
        ["Build Muscle", "Lose Weight", "Improve Cardio"]
    )

    if st.button("Signup"):

        try:
            create_user(name, age, gender, email, password, goal)

            st.success("Account created successfully!")

            st.session_state.page = "login"
            st.rerun()

        except:
            st.error("User already exists")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# -----------------------------
# OTP VERIFICATION PAGE
# -----------------------------
elif st.session_state.page == "otp":

    st.title("OTP Verification")

    user_otp = st.text_input("Enter OTP")

    if st.button("Verify OTP"):

        if user_otp == st.session_state.otp:

            token = create_jwt(st.session_state.email)

            st.session_state.token = token
            st.session_state.page = "dashboard"

            st.success("Login Successful!")
            st.rerun()

        else:
            st.error("Invalid OTP")

# -----------------------------
# DASHBOARD
# -----------------------------
elif st.session_state.page == "dashboard":

    if "token" not in st.session_state:

        st.session_state.page = "login"
        st.rerun()

    st.title("🏋️ Welcome to FitPlan AI Dashboard")

    st.success("You are logged in successfully!")

    st.write("Here you can generate your personalized workout plan.")

    if st.button("Logout"):

        del st.session_state.token
        st.session_state.page = "login"
        st.rerun()