import streamlit as st
import random
from auth import create_jwt, verify_jwt, send_otp_via_sendgrid

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
        
        # New Login Method Toggle
        login_method = st.radio("Login via", ["Password", "OTP"], horizontal=True)
        email = st.text_input("Email Address")
        
        if login_method == "Password":
            password = st.text_input("Password", type="password")
            if st.button("LOGIN"):
                st.session_state.page = "dashboard"
                st.rerun()
        else: # This is the "OTP" branch of your login_method
            if st.button("Generate OTP"):
                if email:
                    # Generate the OTP
                    otp = str(random.randint(100000, 999999))
                    st.session_state.generated_otp = otp
                    
                    # Call SendGrid from your auth.py
                    if send_otp_via_sendgrid(email, otp):
                        st.success("OTP sent to your email!")
                    else:
                        st.error("Failed to send email. Check API Key.")
                else:
                    st.warning("Please enter your email first.")
            
            user_otp = st.text_input("Enter OTP")
            
            if st.button("Verify & Login"):
                # 1. Check if OTP matches
                if user_otp == st.session_state.get("generated_otp") and user_otp != "":
                    
                    # 2. Generate the JWT token
                    token = create_jwt(email)
                    
                    # 3. Store the token and redirect
                    st.session_state.token = token
                    st.session_state.page = "dashboard"
                    st.success("Verified! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid OTP. Please try again.")

        st.markdown("---")

        if st.button("Create New Account"):
            st.session_state.page = "signup"
            st.rerun() 
# =====================================================
# SIGNUP PAGE (Data Collection)
# =====================================================
elif st.session_state.page == "signup":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h2 style='text-align:center'>CREATE ACCOUNT</h2>", unsafe_allow_html=True)
        
        with st.form("registration_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", 10, 80)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            email = st.text_input("Email Address")
            password = st.text_input("Create Password", type="password")
            goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Improve Cardio", "Flexibility"])
            
            if st.form_submit_button("SIGN UP"):
                # Here you would add your DB saving logic
                st.success("Account Created Successfully! 🎉")
                st.session_state.page = "login"
                st.rerun()
        
        if st.button("Already have an account? Login"):
            st.session_state.page = "login"
            st.rerun()
            
# =====================================================
# DASHBOARD – WORKOUT PLAN GENERATOR
# =====================================================
elif st.session_state.page == "dashboard":
    # 1. The Security Guard (Check for token)
    if "token" not in st.session_state:
        st.error("Please log in first.")
        st.session_state.page = "login"
        st.rerun()

    # 2. The Actual Content (If token exists, this runs)
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
        # Clear the token on logout so they must re-verify next time
        del st.session_state.token
        st.session_state.page = "login"
        st.rerun()