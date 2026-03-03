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
    background-image: linear-gradient(rgba(0,0,0,0.80), rgba(0,0,0,0.80)), 
                      url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 0rem;
}}

.card {{
    width: 500px;
    margin: 100px auto;
    padding: 40px;
    background: rgba(0, 0, 0, 0.70);
    border-radius: 12px;
    text-align: center;
    color: white;
}}

.stButton>button {{
    width: 100%;
    background-color: #e50914;
    color: white;
    height: 45px;
    font-weight: bold;
}}

</style>
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

    if st.button("LOGIN"):
        if email and password:
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Please enter Email and Password")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = "signup"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# SIGNUP PAGE
# =====================================================
elif st.session_state.page == "signup":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2>CREATE ACCOUNT</h2>", unsafe_allow_html=True)

    new_email = st.text_input("Email Address")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("SIGN UP"):
        if not new_email or not new_password:
            st.error("Please fill all fields")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            st.success("Account Created Successfully 🎉")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# DASHBOARD – FITPLAN AI MODULE
# =====================================================
elif st.session_state.page == "dashboard":

    st.title("💪 FitPlan AI - Personalized Fitness Plan Generator")

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

    if st.button("Generate Workout Plan"):

        st.subheader("🏋️ Your Personalized Weekly Plan")

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
                st.write(f"- {ex} – 3 sets x 12 reps")

            st.write("Rest: 60 seconds")
            st.markdown("---")

    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()