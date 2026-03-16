import streamlit as st
import random
import database as db
from auth import create_jwt, verify_jwt, send_otp_via_brevo
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

.stApp {
    background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
    color: #ffffff;
}

/* Inputs - Combined and forced white text */
div[data-baseweb="input"] > div, 
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"] > input,
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
}

/* Specific fix for focus visibility */
.stTextInput input:focus, .stNumberInput input:focus {
    background-color: rgba(255, 255, 255, 0.15) !important;
    color: #ffffff !important;
    border-color: #FF4D4D !important;
}

/* Label and Text visibility */
label, .stMarkdown, p, h1, h2, h3, span, [data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
}

.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 2rem;
}

.stButton>button {
    background: linear-gradient(135deg, #FF4D4D 0%, #F9CB28 100%);
    color: white !important;
    border: none !important;
    padding: 0.8rem 2rem !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    width: 100%;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.8s ease-out forwards;
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

# ================= PAGES =================
if st.session_state.page == "landing":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=120)
        st.markdown('<h1 class="hero-text">FIT EVERYWHERE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:1.5rem; color:#CBD5E0">Your AI Powered Fitness Coach.</p>', unsafe_allow_html=True)
        if st.button("GET STARTED"):
            st.session_state.page = "signup"
            st.rerun()
        if st.button("LOG IN", key="l_login"):
            st.session_state.page = "login"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "login":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2>Welcome Back</h2>', unsafe_allow_html=True)
        method = st.radio("Access Method", ["Password", "OTP"], horizontal=True)
        email = st.text_input("Email", placeholder="name@example.com")
        if method == "Password":
            password = st.text_input("Password", type="password")
            if st.button("CONTINUE"):
                user = db.verify_user(email, password)
                if user:
                    st.session_state.user_email = email
                    st.session_state.token = create_jwt(email)
                    profile = db.get_user_profile(email)
                    if profile:
                        st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.goal = profile
                        st.session_state.page = "dashboard"
                    else: st.session_state.page = "profile_setup"
                    st.rerun()
                else: st.error("Fail")
        else:
            if st.button("SEND OTP"):
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                send_otp_via_brevo(email, otp)
                st.success("Sent!")
            entered = st.text_input("Code")
            if st.button("VERIFY"):
                if entered == st.session_state.generated_otp:
                    st.session_state.user_email = email
                    st.session_state.token = create_jwt(email)
                    st.session_state.page = "dashboard"
                    st.rerun()
        if st.button("Need account? Signup"):
            st.session_state.page = "signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "signup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2>Join FitPlan AI</h2>', unsafe_allow_html=True)
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("REGISTER"):
            otp = str(random.randint(100000, 999999))
            st.session_state.generated_otp = otp
            st.session_state.temp_signup = {"name": name, "email": email, "password": password}
            send_otp_via_brevo(email, otp)
            st.session_state.page = "verify_signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "verify_signup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        entered = st.text_input("Enter Code")
        if st.button("COMPLETE"):
            if entered == st.session_state.generated_otp:
                data = st.session_state.temp_signup
                db.add_user(data["name"], 25, "Other", data["email"], data["password"], "Fitness")
                st.session_state.user_email = data["email"]
                st.session_state.name = data["name"]
                st.session_state.page = "profile_setup"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "profile_setup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2>Setup Profile</h2>', unsafe_allow_html=True)
        age = st.number_input("Age", 10, 100, 25)
        height = st.number_input("Height (cm)", 100, 250, 175)
        weight = st.number_input("Weight (kg)", 30, 300, 75)
        goal = st.selectbox("Goal", ["Build Muscle", "Lose Weight", "Endurance"])
        if st.button("FINISH"):
            db.update_profile(st.session_state.name, age, "Male", goal, st.session_state.user_email)
            st.session_state.age, st.session_state.height, st.session_state.weight, st.session_state.goal = age, height, weight, goal
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    st.markdown(f"### 💪 Welcome, {st.session_state.name}")
    if st.sidebar.button("LOGOUT"):
        st.session_state.clear()
        st.session_state.page = "landing"
        st.rerun()
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔥 Workouts", "⚖️ Progress"])
    with tab1:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.write(f"Logged in as {st.session_state.user_email}")
        st.write(f"Goal: {st.session_state.goal}")
        st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        if st.button("GENERATE WORKOUT"):
            with st.spinner("Thinking..."):
                plan = model.generate_workout(st.session_state.name, st.session_state.age, st.session_state.goal, "Beginner", "Full Gym", 22)
                st.markdown(plan)
        st.markdown('</div>', unsafe_allow_html=True)
