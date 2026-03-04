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
    padding-top: 2rem;
}}

.card {{
    width:420px;
    margin:auto;
    margin-top:120px;
    padding:40px;
    background: rgba(0,0,0,0.75);
    border-radius:12px;
    text-align:center;
    color:white;
}}

h2 {{
    color: #FFD700;
    font-weight: bold;
}}

label {{
    color: #FFD700 !important;
    font-weight: 600;
    font-size: 16px;
}}

.stButton>button {{
    width: 100%;
    background-color: #e50914;
    color: white;
    height: 45px;
    font-weight: bold;
    border-radius: 6px;
}}

.stButton>button:hover {{
    background-color: #ff1f2e;
    color: white;
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
# SESSION STATE
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# =====================================================
# LOGIN PAGE
# =====================================================
if st.session_state.page == "login":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2>PLEASE LOG IN</h2>", unsafe_allow_html=True)

    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    login = st.button("LOGIN")

    if login:
        if email and password:
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Please enter Email and Password")

    signup = st.button("Don't have an account? Sign Up")

    if signup:
        st.session_state.page = "signup"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# SIGNUP PAGE
# =====================================================
elif st.session_state.page == "signup":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2>CREATE ACCOUNT</h2>", unsafe_allow_html=True)

    new_email = st.text_input("Email Address")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    signup_btn = st.button("SIGN UP")

    if signup_btn:
        if not new_email or not new_password:
            st.error("Please fill all fields")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            st.success("Account Created Successfully 🎉")
            st.session_state.page = "login"
            st.rerun()

    login_btn = st.button("Already have an account? Login")

    if login_btn:
        st.session_state.page = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# DASHBOARD – FITPLAN AI MODULE
# =====================================================
elif st.session_state.page == "dashboard":

    st.title("💪 FitPlan AI - Personalized Fitness Plan Generator")

    st.subheader("Enter Your Personal Details")

    # Personal Details
    name = st.text_input("Your Name")
    age = st.number_input("Age", min_value=10, max_value=80)
    height = st.number_input("Height (cm)", min_value=100, max_value=220)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200)

    st.subheader("Enter Your Fitness Details")

    goal = st.selectbox(
        "Select Your Goal",
        ["Build Muscle", "Lose Weight", "Improve Cardio", "Increase Flexibility"]
    )

    equipment = st.selectbox(
        "Available Equipment",
        ["No Equipment", "Dumbbells", "Gym Equipment", "Resistance Bands"]
    )

    level = st.selectbox(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    generate = st.button("Generate Workout Plan")

    if generate:

        if not name:
            st.error("Please enter your name")
        else:
            # BMI Calculation
            height_m = height / 100
            bmi = round(weight / (height_m ** 2), 2)

            if bmi < 18.5:
                bmi_status = "Underweight"
            elif bmi < 24.9:
                bmi_status = "Normal"
            elif bmi < 29.9:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"

            st.success(f"Hello {name}! Here is your personalized plan 💪")
            st.write(f"**Your BMI:** {bmi} ({bmi_status})")

            # Personalization Logic
            if weight > 85:
                reps = "15 reps"
            elif weight < 55:
                reps = "10 reps"
            else:
                reps = "12 reps"

            if age > 50:
                rest_time = "90 seconds"
            else:
                rest_time = "60 seconds"

            st.subheader("🏋️ Your Personalized 5-Day Plan")

            for day in range(1, 6):
                st.markdown(f"### Day {day}")

                if goal == "Build Muscle":
                    exercises = ["Push-ups", "Squats", "Bench Press", "Deadlifts", "Bicep Curls"]
                elif goal == "Lose Weight":
                    exercises = ["Jumping Jacks", "Burpees", "Mountain Climbers", "High Knees"]
                elif goal == "Improve Cardio":
                    exercises = ["Running", "Cycling", "Skipping", "Rowing"]
                else:
                    exercises = ["Yoga Stretch", "Hamstring Stretch", "Shoulder Mobility"]

                selected = random.sample(exercises, min(3, len(exercises)))

                for ex in selected:
                    st.write(f"- {ex} – 3 sets x {reps}")

                st.write(f"Rest: {rest_time}")
                st.markdown("---")

    logout = st.button("Logout")

    if logout:
        st.session_state.page = "login"
        st.rerun()