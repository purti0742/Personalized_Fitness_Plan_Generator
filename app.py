import streamlit as st
import random
import database as db
from auth import create_jwt, verify_jwt, send_otp_via_sendgrid
import model

# -----------------------
# INITIALIZE DB
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
# CUSTOM CSS
# -----------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.stApp {
    background: linear-gradient(135deg,#fdfbfb,#ebedee);
}
.navbar {
    display: flex;
    justify-content: space-between;
    padding: 10px 5% 30px 5%;
}
[data-testid="column"] {
    padding: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# SESSION STATES
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

if "signup_temp_data" not in st.session_state:
    st.session_state.signup_temp_data = {}

if "user_email" not in st.session_state:
    st.session_state.user_email = None


# =====================================================
# LOGIN PAGE
# =====================================================
if st.session_state.page == "login":

    _, main_col, _ = st.columns([1,4,1])

    with main_col:

        col1, col2 = st.columns([1,1])

        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=150)
            st.markdown("# FIT EVERYWHERE")
            st.markdown("### Your AI Powered Fitness Companion")
            st.write("Generate personalized workout plans based on:")
            st.markdown("* Age\n* Weight\n* Fitness Level\n* Equipment Availability")

        with col2:

            st.markdown("<h1 style='color:#ff5e62;'>Sign In</h1>", unsafe_allow_html=True)

            login_method = st.radio("Login via", ["Password","OTP"], horizontal=True)

            email = st.text_input("Email")

            if login_method == "Password":

                password = st.text_input("Password", type="password")

                if st.button("LOGIN"):

                    user = db.verify_user(email,password)

                    if user:
                        st.session_state.user_email = email
                        st.session_state.token = create_jwt(email)
                        st.session_state.page = "dashboard"
                        st.rerun()

                    else:
                        st.error("Invalid login")

            else:

                if st.button("Generate OTP"):

                    otp = str(random.randint(100000,999999))
                    st.session_state.generated_otp = otp

                    if send_otp_via_sendgrid(email,otp):
                        st.success("OTP Sent")

                user_otp = st.text_input("Enter OTP")

                if st.button("Verify & Login"):

                    if user_otp == st.session_state.generated_otp:

                        st.session_state.user_email = email
                        st.session_state.token = create_jwt(email)
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

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        st.markdown("## CREATE ACCOUNT")

        name = st.text_input("Full Name")
        age = st.number_input("Age",10,80)
        gender = st.selectbox("Gender",["Male","Female","Other"])
        email = st.text_input("Email Address")
        password = st.text_input("Password",type="password")
        goal = st.selectbox("Goal",["Build Muscle","Lose Weight","Improve Cardio"])

        if st.button("Send OTP"):

            otp = str(random.randint(100000,999999))
            st.session_state.generated_otp = otp

            st.session_state.signup_temp_data = {
                "name":name,
                "age":age,
                "gender":gender,
                "email":email,
                "password":password,
                "goal":goal
            }

            send_otp_via_sendgrid(email,otp)

            st.success("OTP Sent")

        verify = st.text_input("Enter OTP")

        if st.button("Verify & Signup"):

            if verify == st.session_state.generated_otp:

                d = st.session_state.signup_temp_data

                db.add_user(
                    d['name'],
                    d['age'],
                    d['gender'],
                    d['email'],
                    d['password'],
                    d['goal']
                )

                st.success("Account Created")

                st.session_state.page="login"
                st.rerun()

            else:
                st.error("Invalid OTP")

        if st.button("Back to Login"):
            st.session_state.page="login"
            st.rerun()



# =====================================================
# DASHBOARD
# =====================================================
elif st.session_state.page == "dashboard":

    st.title("🏋️ FitPlan AI - Personalized Fitness Planner")

    tabs = st.tabs(["Dashboard","Profile","Workout Plan","Weight Tracker","Logout"])

    # -------------------------------------------------
    # DASHBOARD TAB
    # -------------------------------------------------
    with tabs[0]:

        st.subheader("Welcome")

        st.info(f"Logged in as {st.session_state.user_email}")

        st.write("Use the menu to manage your fitness journey.")



    # -------------------------------------------------
    # PROFILE TAB
    # -------------------------------------------------
    with tabs[1]:

        st.subheader("Profile")

        name = st.text_input("Name")
        age = st.number_input("Age",10,80)
        height = st.number_input("Height (cm)",100,220)
        weight = st.number_input("Weight (kg)",30,200)

        if st.button("Update Profile"):
            st.success("Profile Updated")



    # -------------------------------------------------
    # WORKOUT PLAN TAB
    # -------------------------------------------------
    with tabs[2]:

        st.subheader("Generate Workout Plan")

        goal = st.selectbox(
            "Goal",
            ["Build Muscle","Lose Weight","Improve Cardio","Flexibility"]
        )

        equipment = st.selectbox(
            "Equipment",
            ["No Equipment","Dumbbells","Gym Equipment"]
        )

        level = st.selectbox(
            "Fitness Level",
            ["Beginner","Intermediate","Advanced"]
        )

        if st.button("Generate AI Workout Plan"):

            height_m = height / 100 if height > 0 else 1.7

            bmi = round(weight / (height_m**2),2)

            bmi_status = "Normal"

            if bmi > 25:
                bmi_status="Overweight"

            plan = model.generate_workout(
                name,
                age,
                goal,
                level,
                equipment,
                bmi_status
            )

            st.success("Workout Plan Generated")

            st.info(plan)

            db.save_workout(
                st.session_state.user_email,
                goal,
                plan
            )



    # -------------------------------------------------
    # WEIGHT TRACKER TAB
    # -------------------------------------------------
    with tabs[3]:

        st.subheader("Weight Tracker")

        today_weight = st.number_input(
            "Enter today's weight",
            30.0,
            200.0
        )

        if st.button("Save Weight"):

            db.save_weight(
                st.session_state.user_email,
                today_weight
            )

            st.success("Weight Saved")

        st.subheader("Weight History")

        weights = db.get_weights(
            st.session_state.user_email
        )

        if weights:
            st.line_chart(weights)
        else:
            st.info("No weight records found")



    # -------------------------------------------------
    # LOGOUT TAB
    # -------------------------------------------------
    with tabs[4]:

        st.subheader("Logout")

        if st.button("Logout"):

            st.session_state.clear()

            st.session_state.page="login"

            st.rerun()