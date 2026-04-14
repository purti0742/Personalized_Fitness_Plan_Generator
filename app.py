import streamlit as st
import random
import database as db
from auth import create_jwt, verify_jwt, send_otp_via_brevo
from remember import save_email, load_email
import model
import time

# ---------------- INIT DB ----------------
try:
    db.init_db()
except Exception as e:
    st.error(f"Database Initialization Error: {e}")
    st.stop()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FitPlan AI | Your AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- PREMIUM GLASS THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

* {
    font-family: 'Outfit', sans-serif;
}

/* Force dark background on the entire app and all sub-containers */
.stApp, .main, .block-container {
    background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460) !important;
    color: #ffffff !important;
}

/* Glassmorphism containers */
.glass-card {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 2rem;
    transition: transform 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Premium Buttons */
.stButton>button {
    background: linear-gradient(135deg, #FF4D4D 0%, #F9CB28 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.8rem 2rem !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100%;
    box-shadow: 0 4px 15px rgba(255, 77, 77, 0.3) !important;
}

/* UNIVERSAL UI OVERRIDE - High Contrast */
div[data-baseweb="input"], 
div[data-baseweb="base-input"],
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
input, select, textarea {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Fix for Workout Plan White Background */
.workout-plan-container {
    background: rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 20px;
    margin-bottom: 20px;
    color: #ffffff !important;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
}

.workout-plan-container h1, .workout-plan-container h2, .workout-plan-container h3 {
    color: #F9CB28 !important;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    color: #ffffff !important;
    background-color: transparent !important;
}

.stTabs [aria-selected="true"] {
    background-color: #FF4D4D !important;
    border-radius: 8px !important;
}

/* Text Consistency */
label, p, span, h1, h2, h3, .stMarkdown {
    color: #ffffff !important;
}

.hero-text {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(to right, #ffffff, #FF4D4D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATES ----------------
defaults = {
    "page": "landing",
    "generated_otp": None,
    "user_email": None,
    "temp_signup": None,
    "name": "",
    "age": 20,
    "gender": "Male",
    "goal": "Build Muscle",
    "height": 170,
    "weight": 70,
    "token": None
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= LANDING PAGE =================
if st.session_state.page == "landing":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=120)
        st.markdown('<h1 class="hero-text">FIT EVERYWHERE</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-hero">Your Intelligent AI-Powered Fitness Companion. Personalized plans, real-time tracking, and expert guidance.</p>', unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("GET STARTED"):
                st.session_state.page = "signup"
                st.rerun()
        with btn_col2:
            if st.button("LOG IN", key="landing_login"):
                st.session_state.page = "login"
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================= LOGIN =================
elif st.session_state.page == "login":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center;">Welcome Back</h2>', unsafe_allow_html=True)
        method = st.radio("Access Method", ["Password", "OTP"], horizontal=True)
        email = st.text_input("Email Address", value=load_email(), placeholder="name@example.com")

        if method == "Password":
            password = st.text_input("Password", type="password", placeholder="••••••••")
            if st.button("CONTINUE"):
                user = db.verify_user(email, password)
                if user:
                    save_email(email)
                    st.session_state.user_email = email
                    st.session_state.token = create_jwt(email)
                    profile = db.get_user_profile(email)
                    if profile:
                        st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.height, st.session_state.weight, st.session_state.goal = profile
                        st.session_state.page = "dashboard"
                    else:
                        st.session_state.page = "profile_setup"
                    st.rerun()
                else:
                    st.error("Authentication failed.")
        else:
            if st.button("SEND OTP"):
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                if send_otp_via_brevo(email, otp):
                    st.success("OTP sent!")
                else:
                    st.error("Failed to send OTP.")
            entered = st.text_input("Verification Code", placeholder="123456")
            if st.button("VERIFY"):
                if entered == st.session_state.generated_otp:
                    save_email(email)
                    st.session_state.user_email = email
                    st.session_state.token = create_jwt(email)
                    profile = db.get_user_profile(email)
                    if profile:
                        st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.height, st.session_state.weight, st.session_state.goal = profile
                        st.session_state.page = "dashboard"
                    else:
                        st.session_state.page = "profile_setup"
                    st.rerun()

        if st.button("Need an account? Sign Up"):
            st.session_state.page = "signup"
            st.rerun()
        if st.button("← Back to Home"):
            st.session_state.page = "landing"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================= SIGNUP =================
elif st.session_state.page == "signup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">Join FitPlan AI</h2>', unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email Address", placeholder="john@example.com")
        password = st.text_input("Create Password", type="password", placeholder="Minimum 8 characters")
        if st.button("REGISTER"):
            if name and email and password:
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                st.session_state.temp_signup = {"name": name, "email": email, "password": password}
                if send_otp_via_brevo(email, otp):
                    st.session_state.page = "verify_signup"
                    st.rerun()
        if st.button("Already have an account? Log In"):
            st.session_state.page = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================= VERIFY SIGNUP =================
elif st.session_state.page == "verify_signup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2>Verify Your Email</h2>', unsafe_allow_html=True)
        entered = st.text_input("Enter 6-digit Code")
        if st.button("COMPLETE REGISTRATION"):
            if entered == st.session_state.generated_otp:
                data = st.session_state.temp_signup
                ok = db.add_user(data["name"], 20, "Other", 170.0, 70.0, data["email"], data["password"], "General Fitness")
                if ok:
                    save_email(data["email"])
                    st.session_state.user_email = data["email"]
                    st.session_state.name = data["name"]
                    st.session_state.page = "profile_setup"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PROFILE SETUP =================
elif st.session_state.page == "profile_setup":
    _, main_col, _ = st.columns([1,2,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2>Optimize Your Experience</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 10, 100, 25)
            gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
            height = st.number_input("Height (cm)", 100, 250, 175)
        with col2:
            weight = st.number_input("Weight (kg)", 30, 300, 75)
            goal = st.selectbox("Primary Fitness Goal", ["Build Muscle", "Lose Weight", "Endurance", "Flexibility", "General Fitness"])
        if st.button("FINISH SETUP"):
            db.update_profile(st.session_state.name, age, gender, height, weight, goal, st.session_state.user_email)
            st.session_state.age, st.session_state.gender, st.session_state.goal, st.session_state.height, st.session_state.weight = age, gender, goal, height, weight
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":
    head_col1, head_col2 = st.columns([4,1])
    with head_col1:
        st.markdown(f"### 💪 Welcome, {st.session_state.name}")
    with head_col2:
        if st.button("LOGOUT"):
            st.session_state.clear()
            st.session_state.page = "landing"
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔥 Workout Generator", "⚖️ Progress Tracker", "👤 Profile"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        height_m = st.session_state.height/100
        bmi = round(st.session_state.weight/(height_m**2), 1)
        with col1:
            st.markdown(f'<div class="glass-card" style="text-align: center;"><h4>BMI</h4><h2 style="color: #FF4D4D;">{bmi}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="glass-card" style="text-align: center;"><h4>Weight</h4><h2 style="color: #F9CB28;">{st.session_state.weight} kg</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="glass-card" style="text-align: center;"><h4>Progress</h4><h2 style="color: #4DFF88;">65%</h2></div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            local_goal = st.selectbox("Focus", ["Full Body", "Upper Body", "Lower Body", "Core", "HIIT"], key="gen_goal")
            equipment = st.selectbox("Equipment", ["No Equipment", "Dumbbells Only", "Full Gym", "Kettlebells"])
        with col2:
            level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], index=1)
            intensity = st.select_slider("Intensity", ["Low", "Moderate", "High", "Extreme"], value="Moderate")
        
        if st.button("GENERATE AI PLAN"):
            with st.spinner("Crafting plan..."):
                height_m = st.session_state.height/100
                bmi_val = round(st.session_state.weight/(height_m**2), 2)
                plan = model.generate_workout(st.session_state.name, st.session_state.age, local_goal, level, equipment, bmi_val)
                st.session_state.last_plan = plan
                db.save_workout(st.session_state.user_email, local_goal, plan)
                st.markdown(f'<div class="workout-plan-container">{plan}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        new_w = st.number_input("Log Weight (kg)", 30.0, 300.0, float(st.session_state.weight))
        if st.button("LOG WEIGHT"):
            db.save_weight(st.session_state.user_email, new_w, time.strftime("%Y-%m-%d"))
            st.session_state.weight = new_w
            st.rerun()
        data = db.get_weights(st.session_state.user_email)
        if data: st.line_chart(data)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown("### Profile Settings")
        # Profile update logic here
        st.markdown('</div>', unsafe_allow_html=True)