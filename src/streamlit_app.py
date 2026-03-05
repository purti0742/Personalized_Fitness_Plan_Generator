import streamlit as st
import random

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="FitPlan AI",
    page_icon="💪",
    layout="wide"
)

# -----------------------
# BACKGROUND IMAGE
# -----------------------
bg_url = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=1920&q=80"

# -----------------------
# CUSTOM CSS
# -----------------------
st.markdown(f"""
<style>
.stApp {{
background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
url("{bg_url}");
background-size: cover;
background-position: center;
background-attachment: fixed;
}}

.block-container {{
padding-top: 120px;
}}

h2 {{
color:#FFD700;
font-weight:bold;
}}

label {{
color:#FFD700 !important;
font-weight:600;
}}

.stButton>button {{
width:100%;
background:#e50914;
color:white;
height:45px;
border-radius:6px;
font-weight:bold;
}}

.stButton>button:hover {{
background:#ff1f2e;
}}

.navbar{{
position:fixed;
top:0;
left:0;
width:100%;
height:60px;
background:rgba(0,0,0,0.9);
display:flex;
justify-content:space-between;
align-items:center;
padding:0 40px;
z-index:999;
}}

.navbar-title{{
color:white;
font-weight:bold;
font-size:18px;
}}

.navbar-menu{{
color:white;
font-size:14px;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------
# NAVBAR
# -----------------------
st.markdown("""
<div class="navbar">
<div class="navbar-title">FIT EVERYWHERE</div>
<div class="navbar-menu">Home &nbsp;&nbsp; My Progress &nbsp;&nbsp; Contact</div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# SESSION STATES
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# =====================================================
# LOGIN PAGE
# =====================================================
if st.session_state.page == "login":

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<h2 style='text-align:center'>PLEASE LOG IN</h2>", unsafe_allow_html=True)

        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        login = st.button("LOGIN")

        if login:
            if email and password:
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Enter Email and Password")

        signup = st.button("Don't have an account? Sign Up")

        if signup:
            st.session_state.page = "signup"
            st.rerun()

# =====================================================
# SIGNUP PAGE WITH OTP
# =====================================================
elif st.session_state.page == "signup":

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<h2 style='text-align:center'>CREATE ACCOUNT</h2>", unsafe_allow_html=True)

        new_email = st.text_input("Email Address")

        if st.button("Generate OTP"):

            if new_email:
                otp = random.randint(100000,999999)
                st.session_state.generated_otp = otp
                st.session_state.otp_sent = True

                print("OTP:", otp)   # terminal output

                st.success("OTP Sent (Check terminal for demo)")
            else:
                st.error("Enter email first")

        if st.session_state.otp_sent:

            user_otp = st.text_input("Enter OTP")

            if st.button("Verify OTP"):

                if str(user_otp) == str(st.session_state.generated_otp):
                    st.session_state.otp_verified = True
                    st.success("Email Verified")
                else:
                    st.error("Invalid OTP")

        if st.session_state.otp_verified:

            new_password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            signup_btn = st.button("SIGN UP")

            if signup_btn:

                if new_password != confirm_password:
                    st.error("Passwords do not match")

                else:
                    st.success("Account Created Successfully 🎉")

                    st.session_state.page = "login"
                    st.session_state.otp_sent = False
                    st.session_state.otp_verified = False

                    st.rerun()

        login_btn = st.button("Already have an account? Login")

        if login_btn:
            st.session_state.page = "login"
            st.rerun()

# =====================================================
# DASHBOARD – WORKOUT PLAN GENERATOR
# =====================================================
elif st.session_state.page == "dashboard":

    st.title("💪 FitPlan AI - Personalized Workout Generator")

    st.subheader("Personal Details")

    name = st.text_input("Name")
    age = st.number_input("Age",10,80)
    height = st.number_input("Height (cm)",100,220)
    weight = st.number_input("Weight (kg)",30,200)

    st.subheader("Fitness Details")

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

    generate = st.button("Generate Workout Plan")

    if generate:

        height_m = height/100
        bmi = round(weight/(height_m**2),2)

        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 24.9:
            bmi_status = "Normal"
        elif bmi < 29.9:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

        st.success(f"Hello {name} 💪")
        st.write(f"Your BMI: {bmi} ({bmi_status})")

        if weight > 85:
            reps = "15 reps"
        elif weight < 55:
            reps = "10 reps"
        else:
            reps = "12 reps"

        if age > 50:
            rest = "90 sec"
        else:
            rest = "60 sec"

        st.subheader("🏋️ Your 5-Day Plan")

        for day in range(1,6):

            st.markdown(f"### Day {day}")

            if goal == "Build Muscle":
                exercises = ["Push-ups","Squats","Bench Press","Deadlifts","Bicep Curls"]

            elif goal == "Lose Weight":
                exercises = ["Burpees","Jump Rope","Mountain Climbers","High Knees"]

            elif goal == "Improve Cardio":
                exercises = ["Running","Cycling","Skipping","Rowing"]

            else:
                exercises = ["Yoga Stretch","Hamstring Stretch","Shoulder Mobility"]

            selected = random.sample(exercises,3)

            for ex in selected:
                st.write(f"- {ex} – 3 sets x {reps}")

            st.write(f"Rest: {rest}")
            st.markdown("---")

    logout = st.button("Logout")

    if logout:
        st.session_state.page = "login"
        st.rerun()