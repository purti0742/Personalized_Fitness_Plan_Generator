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
    page_title="FitPlan AI | Pro Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- PREMIUM GLASS THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp {
    background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
    color: #ffffff;
}

.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 28px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.glass-card:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.2);
}

.stButton>button {
    background: linear-gradient(135deg, #FF4D4D 0%, #F9CB28 100%);
    color: white !important;
    border: none !important;
    padding: 0.8rem 2rem !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton>button:hover {
    box-shadow: 0 10px 25px rgba(255, 77, 77, 0.4) !important;
    transform: scale(1.03);
}

.hero-text {
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(to right, #ffffff, #FF4D4D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem;
}

/* High Contrast Form Elements */
div[data-baseweb="input"], input, select, textarea {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
}

label p { font-size: 1.1rem !important; color: #E2E8F0 !important; margin-bottom: 8px !important; }

.fade-in { animation: fadeIn 1s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATES ----------------
if "page" not in st.session_state:
    st.session_state.update({
        "page": "landing",
        "user_email": None,
        "name": "",
        "age": 25,
        "gender": "Other",
        "height": 175.0,
        "weight": 70.0,
        "goal": "General Fitness",
        "token": None
    })

# ================= NAVIGATION =================
def nav_to(page):
    st.session_state.page = page
    st.rerun()

# ================= LANDING PAGE =================
if st.session_state.page == "landing":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=120)
        st.markdown('<h1 class="hero-text">EVOLVE <br>TODAY</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.4rem; color: #94A3B8; margin-bottom: 3rem;">Experience AI-driven fitness coaching tailored to your biology and goals. Science-backed, premium guidance.</p>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("GET STARTED"): nav_to("signup")
        with c2:
            if st.button("LOGIN"): nav_to("login")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= AUTH LOGIC (LOGIN/SIGNUP) =================
elif st.session_state.page in ["login", "signup", "verify_signup"]:
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown(f'<div class="glass-card fade-in">', unsafe_allow_html=True)
        
        if st.session_state.page == "login":
            st.markdown('<h2 style="text-align: center;">Welcome Back</h2><br>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            if st.button("ENTER DASHBOARD"):
                user = db.verify_user(email, password)
                if user:
                    st.session_state.user_email = email
                    profile = db.get_user_profile(email)
                    if profile:
                        st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.height, st.session_state.goal = profile
                        st.session_state.weight = db.get_last_weight(email) or 70.0
                        nav_to("dashboard")
                    else:
                        nav_to("profile_setup")
                else: 
                    st.error("Invalid credentials.")
            if st.button("SWITCH TO SIGNUP"): nav_to("signup")

        elif st.session_state.page == "signup":
            st.markdown('<h2 style="text-align: center;">Create Account</h2><br>', unsafe_allow_html=True)
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("REQUEST OTP"):
                if name and email and password:
                    otp = str(random.randint(100000, 999999))
                    st.session_state.generated_otp = otp
                    st.session_state.temp_signup = {"name": name, "email": email, "password": password}
                    if send_otp_via_brevo(email, otp):
                        nav_to("verify_signup")
                    else: st.error("Email service failed.")
                else: st.warning("Fields required.")
            if st.button("BACK TO LOGIN"): nav_to("login")

        elif st.session_state.page == "verify_signup":
            st.markdown('<h2>Verify Identity</h2>', unsafe_allow_html=True)
            entered = st.text_input("6-digit Code")
            if st.button("VERIFY"):
                if entered == st.session_state.generated_otp:
                    data = st.session_state.temp_signup
                    if db.add_user(data["name"], 25, "Other", 175.0, data["email"], data["password"], "Fitness"):
                        st.session_state.user_email = data["email"]
                        st.session_state.name = data["name"]
                        nav_to("profile_setup")
                    else: st.error("Account exists.")
                else: st.error("Invalid code.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PROFILE SETUP =================
elif st.session_state.page == "profile_setup":
    _, main_col, _ = st.columns([1,2,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in"><h2>Personalize Core</h2><br>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 10, 100, 25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            height = st.number_input("Height (cm)", 100.0, 250.0, 175.0)
        with col2:
            weight = st.number_input("Weight (kg)", 30.0, 300.0, 70.0)
            goal = st.selectbox("Primary Goal", ["Build Muscle", "Lose Weight", "Endurance", "General Fitness"])
        
        if st.button("LOCK PROFILE"):
            db.update_profile(st.session_state.name, age, gender, height, goal, st.session_state.user_email)
            db.save_weight(st.session_state.user_email, weight, time.strftime("%Y-%m-%d"))
            st.session_state.update({"age": age, "gender": gender, "height": height, "weight": weight, "goal": goal})
            nav_to("dashboard")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":
    st.markdown(f"### 💪 Performance Dashboard | {st.session_state.name}")
    
    t1, t2, t3, t4 = st.tabs(["Overview", "AI Trainer", "Analytics", "Settings"])

    with t1:
        c1, c2, c3 = st.columns(3)
        bmi = round(st.session_state.weight / ((st.session_state.height/100)**2), 1)
        with c1:
            st.markdown(f'<div class="glass-card"><h4>BMI Index</h4><h1 style="color:#FF4D4D;">{bmi}</h1></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="glass-card"><h4>Weight</h4><h1 style="color:#F9CB28;">{st.session_state.weight} kg</h1></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="glass-card"><h4>Current Goal</h4><p style="font-size:1.5rem;">{st.session_state.goal}</p></div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="glass-card"><h3>Neural Workout Generator</h3>', unsafe_allow_html=True)
        focus = st.selectbox("Focus Area", ["Full Body", "Upper Body", "Lower Body", "Core", "HIIT"])
        equip = st.selectbox("Equipment", ["No Equipment", "Dumbbells", "Full Gym"])
        lvl = st.select_slider("Intensity Level", ["Beginner", "Intermediate", "Advanced"])
        
        if st.button("GENERATE NEURAL PLAN"):
            with st.spinner("AI is calculating muscle load..."):
                plan = model.generate_workout(st.session_state.name, st.session_state.age, focus, lvl, equip, bmi)
                st.session_state.last_plan = plan
                db.save_workout(st.session_state.user_email, focus, plan)
                st.markdown(plan)
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("Weight Progression")
        hist = db.get_weights(st.session_state.user_email)
        if hist is not None: st.line_chart(hist)
        else: st.info("Start logging weight to see trends.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        if st.button("LOGOUT"):
            st.session_state.clear()
            nav_to("landing")
