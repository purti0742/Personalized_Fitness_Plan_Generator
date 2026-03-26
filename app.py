import streamlit as st
import random
import database as db
from auth import create_jwt, verify_jwt, send_otp_via_brevo
import model
import time
from datetime import datetime

# ---------------- INIT DB ----------------
try:
    db.init_db()
except Exception as e:
    st.error(f"Database Initialization Error: {e}")
    st.stop()

# ---------------- SESSION STATES ----------------
if "theme" not in st.session_state: st.session_state.theme = "Dark"
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
        "food_pref": "None",
        "region": "None",
        "token": None
    })

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FitPlan AI | Ultimate Coach",
    page_icon="💪",
    layout="wide",
)

# ---------------- PREMIUM THEMES (CSS) ----------------
dark_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
* { font-family: 'Outfit', sans-serif; }
.stApp {
    background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
    color: #ffffff;
}
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
.stButton>button {
    background: linear-gradient(135deg, #FF4D4D 0%, #F9CB28 100%);
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
}
div[data-baseweb="input"], input, select, textarea {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}
label p { color: #ffffff !important; font-weight: 600 !important; }
</style>
"""

light_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
* { font-family: 'Outfit', sans-serif; }
.stApp { background: #f1f5f9; color: #1e293b; }
.glass-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
.stButton>button {
    background: #3b82f6;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
}
</style>
"""

st.markdown(dark_css if st.session_state.theme == "Dark" else light_css, unsafe_allow_html=True)

def nav_to(p):
    st.session_state.page = p
    st.rerun()

# ================= AUTHENTICATION PAGES =================
if st.session_state.page == "landing":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h1 style="font-size: 4.5rem; font-weight: 800; text-align: center;">FITPLAN AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.5rem; text-align: center;">Personalized workouts, diets, and habit tracking powered by intelligence.</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("GET STARTED"): nav_to("signup")
        with c2:
            if st.button("LOG IN"): nav_to("login")

elif st.session_state.page == "login":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card"><h2>Welcome Back</h2>', unsafe_allow_html=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            user = db.verify_user(email, password)
            if user:
                st.session_state.user_email = email
                p = db.get_user_profile(email)
                if p:
                    st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.height, st.session_state.goal, st.session_state.food_pref, st.session_state.region = p
                    st.session_state.weight = db.get_last_weight(email) or 70.0
                    nav_to("dashboard")
                else: nav_to("profile_setup")
            else: st.error("Invalid credentials.")
        if st.button("← Back"): nav_to("landing")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "signup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card"><h2>Create Account</h2>', unsafe_allow_html=True)
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("SIGN UP"):
            if name and email and password:
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                st.session_state.temp_signup = {"name": name, "email": email, "password": password}
                if send_otp_via_brevo(email, otp): nav_to("verify_signup")
                else: st.error("Email API failed.")
            else: st.warning("All fields required.")
        if st.button("← Back"): nav_to("landing")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "verify_signup":
    _, main_col, _ = st.columns([1,1.5,1])
    with main_col:
        st.markdown('<div class="glass-card"><h2>Verify Email</h2>', unsafe_allow_html=True)
        entered = st.text_input("6-digit Code")
        if st.button("CONTINUE"):
            if entered == st.session_state.generated_otp:
                d = st.session_state.temp_signup
                if db.add_user(d["name"], 25, "Other", 175.0, d["email"], d["password"], "Fitness"):
                    st.session_state.user_email = d["email"]
                    st.session_state.name = d["name"]
                    nav_to("profile_setup")
            else: st.error("Wrong code.")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "profile_setup":
    _, main_col, _ = st.columns([1,2,1])
    with main_col:
        st.markdown('<div class="glass-card"><h2>Profile Calibration</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 10, 100, 25)
            height = st.number_input("Height (cm)", 100.0, 250.0, 175.0)
            food = st.selectbox("Food Preference", ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Paleo"])
        with col2:
            weight = st.number_input("Weight (kg)", 30.0, 300.0, 70.0)
            goal = st.selectbox("Goal", ["Build Muscle", "Lose Weight", "Endurance", "General Fitness"])
            reg = st.text_input("Region (for diet tips)", value="South Asia")
        if st.button("START JOURNEY"):
            db.update_profile(st.session_state.name, age, "Other", height, goal, food, reg, st.session_state.user_email)
            db.save_weight(st.session_state.user_email, weight, datetime.now().strftime("%Y-%m-%d"))
            st.session_state.update({"age": age, "height": height, "weight": weight, "goal": goal, "food_pref": food, "region": reg})
            nav_to("dashboard")
        st.markdown('</div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":
    st.markdown(f"### 💪 {st.session_state.name}'s Command Center")
    tabs = st.tabs(["📊 Stats", "🔥 Generator", "📚 Library", "💧 Habits", "📈 Analytics", "👤 Profile"])

    with tabs[0]: # Stats Overview
        c1, c2, c3 = st.columns(3)
        bmi = round(st.session_state.weight / ((st.session_state.height/100)**2), 1)
        with c1: st.markdown(f'<div class="glass-card" style="text-align:center;"><h4>BMI INDEX</h4><h2>{bmi}</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="glass-card" style="text-align:center;"><h4>CURRENT WEIGHT</h4><h2>{st.session_state.weight} kg</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="glass-card" style="text-align:center;"><h4>DIET</h4><h2>{st.session_state.food_pref}</h2></div>', unsafe_allow_html=True)

    with tabs[1]: # Workout Generator (PRESERVED FULL LOGIC)
        st.markdown('<div class="glass-card"><h3>AI Dynamic Plan Generator</h3>', unsafe_allow_html=True)
        st.write(f"Tailoring for your **{st.session_state.food_pref}** diet and **{st.session_state.region}** region.")
        col1, col2 = st.columns(2)
        with col1:
            specific_goal = st.selectbox("Specific Workout Focus", ["Full Body", "Upper Body", "Lower Body", "Core", "HIIT"])
            equipment = st.selectbox("Available Equipment", ["No Equipment", "Dumbbells Only", "Full Gym", "Kettlebells"])
        with col2:
            level = st.selectbox("Your Fitness Level", ["Beginner", "Intermediate", "Advanced"], index=1)
            intensity = st.select_slider("Workout Intensity", ["Low", "Moderate", "High", "Extreme"], value="Moderate")

        if st.button("GENERATE PLAN"):
            with st.spinner("AI evolving your plan..."):
                p = model.generate_workout(st.session_state.name, st.session_state.age, specific_goal, level, equipment, bmi, st.session_state.food_pref, st.session_state.region)
                db.save_workout(st.session_state.user_email, specific_goal, p)
                st.markdown(p)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]: # Library (PRESERVED)
        st.markdown('<div class="glass-card"><h3>Historical Training Logs</h3>', unsafe_allow_html=True)
        h = db.get_workouts(st.session_state.user_email)
        if not h.empty:
            for _, r in h.iterrows():
                with st.expander(f"📅 {r['created_at']} | 🎯 {r['focus']}"):
                    st.markdown(r['plan'])
        else: st.info("No saved plans yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]: # Habits (H2O & Challenges)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-card"><h4>Hydration Tracker</h4>', unsafe_allow_html=True)
            ml = st.slider("Log Water Intake (ml)", 0, 1000, 250, 50)
            if st.button("ADD WATER"):
                db.save_water(st.session_state.user_email, ml, datetime.now().strftime("%Y-%m-%d"))
                st.success("H2O Logged!")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="glass-card"><h4>30-Day Challenges</h4>', unsafe_allow_html=True)
            chal = st.text_input("New Challenge Name")
            if st.button("BEGIN CHALLENGE"):
                db.add_challenge(st.session_state.user_email, chal, datetime.now().strftime("%Y-%m-%d"), 30)
                st.success("Let's go!")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]: # Analytics (PRESERVED)
        st.markdown('<div class="glass-card"><h3>Performance Analytics</h3>', unsafe_allow_html=True)
        col_w, col_h = st.columns(2)
        with col_w:
            st.write("Weight Progression")
            w_logs = db.get_weights(st.session_state.user_email)
            if w_logs is not None: st.line_chart(w_logs)
        with col_h:
            st.write("Hydration History")
            h_logs = db.get_water_history(st.session_state.user_email)
            if not h_logs.empty: st.bar_chart(h_logs.set_index("date"))
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[5]: # Profile & Settings
        st.markdown('<div class="glass-card"><h3>Profile & Aesthetics</h3>', unsafe_allow_html=True)
        st.session_state.theme = st.selectbox("Visual Mode", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
        if st.button("APPLY THEME"): st.rerun()
        st.markdown("---")
        u_name = st.text_input("Name", value=st.session_state.name)
        u_age = st.number_input("Age", 10, 100, int(st.session_state.age))
        u_height = st.number_input("Height", 100.0, 250.0, float(st.session_state.height))
        u_weight = st.number_input("Log New Weight", 30.0, 300.0, float(st.session_state.weight))
        u_food = st.text_input("Diet Preference", value=st.session_state.food_pref)
        u_reg = st.text_input("Region", value=st.session_state.region)
        
        if st.button("UPDATE EVERYTHING"):
            db.update_profile(u_name, u_age, st.session_state.gender, u_height, st.session_state.goal, u_food, u_reg, st.session_state.user_email)
            db.save_weight(st.session_state.user_email, u_weight, datetime.now().strftime("%Y-%m-%d"))
            st.session_state.update({"name": u_name, "age": u_age, "height": u_height, "weight": u_weight, "food_pref": u_food, "region": u_reg})
            st.success("All systems updated!")
        
        if st.button("DISCONNECT (LOGOUT)"):
            st.session_state.clear()
            nav_to("landing")
        st.markdown('</div>', unsafe_allow_html=True)
