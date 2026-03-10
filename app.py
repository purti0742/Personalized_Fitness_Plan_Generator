import streamlit as st
import random
from auth import create_jwt, verify_jwt, send_otp_via_sendgrid
import sqlite3

# -----------------------
# DATABASE CONNECTION
# -----------------------
conn = sqlite3.connect("fitplan.db", check_same_thread=False)
cursor = conn.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    age INTEGER,
    gender TEXT,
    email TEXT PRIMARY KEY,
    password TEXT,
    goal TEXT
)
""")

# Create Workout Plan Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS workout_plans(
    email TEXT,
    goal TEXT,
    plan TEXT
)
""")
conn.commit()

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
    padding-bottom: 0rem;
}
.stApp {
    background: linear-gradient(135deg,#fdfbfb,#ebedee);
}
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 5% 30px 5%;
    font-family: 'Source Sans Pro', sans-serif;
}
[data-testid="column"] {
    padding: 0px !important;
    margin: 0px !important;
}
.stTextInput input { border-radius: 8px !important; height: 45px; }
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#ff9966,#ff5e62) !important;
    color: white !important;
    height: 48px;
    border-radius: 10px !important;
    font-weight: 600;
    border: none !important;
    margin-top: 10px;
}
.stButton>button:hover { transform: translateY(-1px); box-shadow: 0 5px 15px rgba(255, 94, 98, 0.4); }
div[role="radiogroup"] { padding: 10px 0; }
</style>
""", unsafe_allow_html=True)

# -----------------------
# SESSION STATES
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

# =====================================================
# LOGIN PAGE
# =====================================================
if st.session_state.page == "login":
    _, main_col, _ = st.columns([1, 4, 1])

    with main_col:
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=150)
            st.markdown("# FIT EVERYWHERE")
            st.markdown("### Your AI Powered Fitness Companion")
            st.markdown("""
            * **Age**
            * **Weight**
            * **Fitness Level**
            * **Equipment Availability**
            """)
            st.info("Stay consistent. Stay strong. 💪")

        with col2:
            st.markdown("<h1 style='color:#ff5e62;'>Sign In</h1>", unsafe_allow_html=True)
            login_method = st.radio("Login via", ["Password", "OTP"], horizontal=True)
            email = st.text_input("Email Address", placeholder="name@example.com")

            if login_method == "Password":
                password = st.text_input("Password", type="password")
                if st.button("LOGIN"):
                    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
                    user = cursor.fetchone()
                    if user:
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
            else:
                if st.button("Generate OTP"):
                    if email:
                        otp = str(random.randint(100000, 999999))
                        st.session_state.generated_otp = otp
                        if send_otp_via_sendgrid(email, otp):
                            st.success("OTP sent successfully!")
                        else:
                            st.error("Email failed.")
                    else:
                        st.warning("Enter email first.")

                user_otp = st.text_input("Enter OTP")
                if st.button("Verify & Login"):
                    if user_otp == st.session_state.get("generated_otp") and user_otp != "":
                        st.session_state.token = create_jwt(email)
                        st.session_state.page = "dashboard"
                        st.success("Login successful!")
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
    col1, col2, col3 = st.columns([1, 2, 1])
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
                cursor.execute("INSERT INTO users (name, age, gender, email, password, goal) VALUES (?,?,?,?,?,?)",
                               (name, age, gender, email, password, goal))
                conn.commit()
                st.success("Account Created Successfully! 🎉")
                st.session_state.page = "login"
                st.rerun()
        
        if st.button("Already have an account? Login"):
            st.session_state.page = "login"
            st.rerun()

# =====================================================
# DASHBOARD
# =====================================================
elif st.session_state.page == "dashboard":
    if "token" not in st.session_state:
        st.error("Please log in first.")
        st.session_state.page = "login"
        st.rerun()

    st.title("💪 FitPlan AI - Personalized Workout Generator")
    
    st.subheader("Personal Details")
    name = st.text_input("Name")
    age = st.number_input("Age", 10, 80)
    height = st.number_input("Height (cm)", 100, 220)
    weight = st.number_input("Weight (kg)", 30, 200)

    st.subheader("Fitness Details")
    goal = st.selectbox("Goal", ["Build Muscle", "Lose Weight", "Improve Cardio", "Flexibility"])
    equipment = st.selectbox("Equipment", ["No Equipment", "Dumbbells", "Gym Equipment"])
    level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Workout Plan"):
        height_m = height/100
        bmi = round(weight/(height_m**2), 2)

        if bmi < 18.5: bmi_status = "Underweight"
        elif bmi < 24.9: bmi_status = "Normal"
        elif bmi < 29.9: bmi_status = "Overweight"
        else: bmi_status = "Obese"

        st.success(f"Hello {name} 💪")
        st.write(f"Your BMI: {bmi} ({bmi_status})")

        reps = "15 reps" if weight > 85 else "10 reps" if weight < 55 else "12 reps"
        rest = "90 sec" if age > 50 else "60 sec"

        st.subheader("🏋️ Your 5-Day Plan")
        for day in range(1, 6):
            st.markdown(f"### Day {day}")
            if goal == "Build Muscle":
                exercises = ["Push-ups", "Squats", "Bench Press", "Deadlifts", "Bicep Curls"]
            elif goal == "Lose Weight":
                exercises = ["Burpees", "Jump Rope", "Mountain Climbers", "High Knees"]
            elif goal == "Improve Cardio":
                exercises = ["Running", "Cycling", "Skipping", "Rowing"]
            else:
                exercises = ["Yoga Stretch", "Hamstring Stretch", "Shoulder Mobility"]

            selected = random.sample(exercises, 3)
            for ex in selected:
                st.write(f"- {ex} – 3 sets x {reps}")
            st.write(f"Rest: {rest}")
            st.markdown("---")

    # -----------------------------
        # SAVE PLAN TO DATABASE HERE
        # -----------------------------
        cursor.execute(
            "INSERT INTO workout_plans (email,goal,plan) VALUES (?,?,?)",
            (email, goal, generated_plan)
        )

        conn.commit()

        st.success("Workout plan saved successfully!")

    if st.button("Logout"):
        del st.session_state.token
        st.session_state.page = "login"
        st.rerun() 