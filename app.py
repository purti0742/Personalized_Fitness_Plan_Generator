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

/* Glassmorphism containers */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
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
    background: linear-gradient(135deg, #FF4D4D 0%, #F9CB28 100%);
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

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(255, 77, 77, 0.5) !important;
}

/* UNIVERSAL UI OVERRIDE - High Contrast */
div[data-baseweb="input"], 
div[data-baseweb="base-input"],
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
input, select, textarea {
    background-color: #1a1a2e !important;
    background: #1a1a2e !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

/* Dropdown list contrast */
ul[role="listbox"] {
    background-color: #1a1a2e !important;
}

li[role="option"] {
    background-color: #1a1a2e !important;
    color: #ffffff !important;
}

li[role="option"]:hover {
    background-color: #FF4D4D !important;
}

/* Slider contrast */
div[data-testid="stThumbValue"] {
    color: #FF4D4D !important;
    font-weight: bold !important;
}

div[data-testid="stTickBar"] span {
    color: #ffffff !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 5px !important;
}

.stTabs [data-baseweb="tab"] {
    color: #ffffff !important;
    opacity: 0.6;
}

.stTabs [aria-selected="true"] {
    opacity: 1 !important;
    background-color: #FF4D4D !important;
    border-radius: 8px !important;
}

/* Label and help text */
label, .stMarkdown, p, h1, h2, h3, span, [data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Card Styling */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 2rem;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.8s ease-out forwards;
}

/* Hero Section */
.hero-text {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(to right, #ffffff, #FF4D4D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}

.sub-hero {
    font-size: 1.5rem;
    color: #CBD5E0;
    margin-bottom: 2rem;
}

h1, h2, h3 {
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATES ----------------
defaults = {
    "page": "landing", # Changed initial page to landing
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
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">Welcome Back</h2>', unsafe_allow_html=True)

        method = st.radio("Access Method", ["Password", "OTP"], horizontal=True)
        email = st.text_input("Email Address", placeholder="name@example.com")

        if method == "Password":
            password = st.text_input("Password", type="password", placeholder="••••••••")
            if st.button("CONTINUE"):
                user = db.verify_user(email, password)
                if user:
                    st.session_state.user_email = email
                    st.session_state.token = create_jwt(email)
                    profile = db.get_user_profile(email)
                    if profile:
                        st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.goal = profile
                        st.session_state.page = "dashboard"
                    else:
                        st.session_state.page = "profile_setup" # Direct to setup if no profile
                    st.rerun()
                else:
                    st.error("Authentication failed. Check credentials.")
        else:
            if st.button("SEND OTP"):
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                if send_otp_via_brevo(email, otp):
                    st.success("OTP sent to your email!")
                else:
                    st.error("Failed to send OTP. Try again.")

            entered = st.text_input("Verification Code", placeholder="123456")
            if st.button("VERIFY"):
                if entered == st.session_state.generated_otp:
                    st.session_state.user_email = email
                    st.session_state.token = create_jwt(email)
                    profile = db.get_user_profile(email)
                    if profile:
                        st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.goal = profile
                        st.session_state.page = "dashboard"
                    else:
                        st.session_state.page = "profile_setup"
                    st.rerun()
                else:
                    st.error("Invalid verification code.")

        st.markdown("<hr style='opacity: 0.1'>", unsafe_allow_html=True)
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
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("REGISTER"):
            if name and email and password:
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                st.session_state.temp_signup = {
                    "name": name, "email": email, "password": password
                }
                if send_otp_via_brevo(email, otp):
                    st.session_state.page = "verify_signup"
                    st.rerun()
                else:
                    st.error("Could not send verification email.")
            else:
                st.warning("Please fill all fields.")

        st.markdown("<hr style='opacity: 0.1'>", unsafe_allow_html=True)
        if st.button("Already have an account? Log In"):
            st.session_state.page = "login"
            st.rerun()
        if st.button("← Back"):
            st.session_state.page = "landing"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ================= VERIFY SIGNUP =================
elif st.session_state.page == "verify_signup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2>Verify Your Email</h2>', unsafe_allow_html=True)
        st.write(f"We've sent a code to {st.session_state.temp_signup['email']}")
        
        entered = st.text_input("Enter 6-digit Code")
        if st.button("COMPLETE REGISTRATION"):
            if entered == st.session_state.generated_otp:
                data = st.session_state.temp_signup
                # Initial signup with default age/gender - will be updated in set up
                ok = db.add_user(data["name"], 20, "Other", data["email"], data["password"], "General Fitness")
                if ok:
                    st.success("Welcome aboard! Let's set up your profile.")
                    st.session_state.user_email = data["email"]
                    st.session_state.name = data["name"]
                    st.session_state.page = "profile_setup"
                    st.rerun()
                else:
                    st.error("Registration failed. Email might be in use.")
            else:
                st.error("Incorrect code.")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= PROFILE SETUP =================
elif st.session_state.page == "profile_setup":
    _, main_col, _ = st.columns([1,2,1])
    with main_col:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2>Optimize Your Experience</h2>', unsafe_allow_html=True)
        st.write("Help us tailor the perfect workout plans for you.")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 10, 100, 25)
            gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
            height = st.number_input("Height (cm)", 100, 250, 175)
        with col2:
            weight = st.number_input("Weight (kg)", 30, 300, 75)
            goal = st.selectbox("Primary Fitness Goal", ["Build Muscle", "Lose Weight", "Endurance", "Flexibility", "General Fitness"])
        
        if st.button("FINISH SETUP"):
            db.update_profile(st.session_state.name, age, gender, goal, st.session_state.user_email)
            st.session_state.age = age
            st.session_state.gender = gender
            st.session_state.goal = goal
            st.session_state.height = height
            st.session_state.weight = weight
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":
    
    # Custom Header
    head_col1, head_col2 = st.columns([4,1])
    with head_col1:
        st.markdown(f"### 💪 Welcome, {st.session_state.name}")
    with head_col2:
        if st.button("LOGOUT"):
            st.session_state.clear()
            st.session_state.page = "landing"
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Overview", "🔥 Workout Generator", "⚖️ Progress Tracker", "👤 Profile"]
    )

    with tab1:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        height_m = st.session_state.height/100
        bmi = round(st.session_state.weight/(height_m**2), 1)
        
        with col1:
            st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
            st.markdown("#### Current BMI")
            st.markdown(f"<h2 style='color: #FF4D4D;'>{bmi}</h2>", unsafe_allow_html=True)
            status = "Normal" if 18.5 <= bmi <= 25 else "Overweight" if bmi > 25 else "Underweight"
            st.write(f"Status: **{status}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
            st.markdown("#### Weight")
            st.markdown(f"<h2 style='color: #F9CB28;'>{st.session_state.weight} kg</h2>", unsafe_allow_html=True)
            st.write(f"Goal: {st.session_state.goal}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
            st.markdown("#### Goal Progress")
            st.markdown("<h2 style='color: #4DFF88;'>65%</h2>", unsafe_allow_html=True)
            st.progress(0.65)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Recent Activity")
        st.info("No workouts generated yet. Start by going to the Workout Generator tab!")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown("### Generate Your AI Workout Plan")
        
        col1, col2 = st.columns(2)
        with col1:
            local_goal = st.selectbox("Specific Workout Focus", ["Full Body", "Upper Body", "Lower Body", "Core", "HIIT"], key="gen_goal")
            equipment = st.selectbox("Available Equipment", ["No Equipment", "Dumbbells Only", "Full Gym", "Kettlebells"])
        with col2:
            level = st.selectbox("Your Fitness Level", ["Beginner", "Intermediate", "Advanced"], index=1)
            intensity = st.select_slider("Workout Intensity", ["Low", "Moderate", "High", "Extreme"], value="Moderate")

        if st.button("GENERATE AI PLAN"):
            with st.spinner("AI is crafting your personalized plan..."):
                height_m = st.session_state.height/100
                bmi_val = round(st.session_state.weight/(height_m**2), 2)
                
                plan = model.generate_workout(
                    st.session_state.name,
                    st.session_state.age,
                    local_goal,
                    level,
                    equipment,
                    bmi_val
                )
                
                st.session_state.last_plan = plan
                db.save_workout(st.session_state.user_email, local_goal, plan)
                st.success("Plan Generated Successfully!")
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(plan)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown("### Weight Progression")
        
        col1, col2 = st.columns([1,2])
        with col1:
            new_w = st.number_input("Log Today's Weight (kg)", 30.0, 300.0, float(st.session_state.weight))
            if st.button("LOG WEIGHT"):
                db.save_weight(st.session_state.user_email, new_w, time.strftime("%Y-%m-%d"))
                st.session_state.weight = new_w
                st.success("Weight logged!")
                st.rerun()
                
        with col2:
            data = db.get_weights(st.session_state.user_email)
            if data:
                st.line_chart(data)
            else:
                st.write("No weight data logged yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown("### Profile Settings")
        
        new_name = st.text_input("Name", value=st.session_state.name)
        new_age = st.number_input("Age", 10, 100, value=st.session_state.age)
        new_height = st.number_input("Height (cm)", 100, 250, value=int(st.session_state.height))
        new_weight = st.number_input("Weight (kg)", 30, 300, value=int(st.session_state.weight))
        new_goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Endurance", "Flexibility", "General Fitness"], 
                               index=["Build Muscle", "Lose Weight", "Endurance", "Flexibility", "General Fitness"].index(st.session_state.goal))

        if st.button("UPDATE PROFILE"):
            db.update_profile(new_name, new_age, st.session_state.gender, new_goal, st.session_state.user_email)
            st.session_state.name = new_name
            st.session_state.age = new_age
            st.session_state.height = new_height
            st.session_state.weight = new_weight
            st.session_state.goal = new_goal
            st.success("Profile updated successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
