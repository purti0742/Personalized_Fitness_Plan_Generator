import streamlit as st
import random
from auth import create_jwt, verify_jwt, send_otp_via_sendgrid
import model

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="FitPlan AI",
    page_icon="💪",
    layout="wide"
)

# -----------------------
# CUSTOM CSS (Corrected for Seamless Split)
# -----------------------
st.markdown("""
<style>
/* Remove default Streamlit padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 0rem;
}
.stApp {
    background: linear-gradient(135deg,#fdfbfb,#ebedee);
}
/* NAVBAR STYLING */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 5% 30px 5%;
    font-family: 'Source Sans Pro', sans-serif;
}
.navbar-title { font-weight: 800; font-size: 22px; color: #333; }
.navbar-menu { font-size: 16px; color: #666; }
/* FIXING COLUMN SPACING FOR SEAMLESS LOOK */
[data-testid="column"] {
    padding: 0px !important;
    margin: 0px !important;
}
/* LEFT PANEL */
.left-panel {
    background: linear-gradient(135deg,#ff9966,#ff5e62);
    border-radius: 20px 0px 0px 20px;
    padding: 60px;
    height: 700px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
}
/* RIGHT PANEL */
.right-panel {
    background: white;
    border-radius: 0px 20px 20px 0px;
    padding: 60px;
    height: 700px;
    box-shadow: 10px 10px 40px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.app-title { font-size: 42px; font-weight: 800; margin-top: 20px; }
.app-desc { font-size: 17px; margin-top: 20px; opacity: 0.9; line-height: 1.6; }
.form-title { font-size: 35px; font-weight: 700; color: #ff5e62; margin-bottom: 20px; }
/* INPUT & BUTTON STYLING */
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
/* Remove Radio Label spacing */
div[role="radiogroup"] { padding: 10px 0; }
</style>
""", unsafe_allow_html=True)

# -----------------------
# NAVBAR
# -----------------------
st.markdown("""
<div class="navbar">
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
if "signup_temp_data" not in st.session_state:
    st.session_state.signup_temp_data = {}

# =====================================================
# LOGIN PAGE (Cleaned UI)
# =====================================================
if st.session_state.page == "login":

    # Using a 3-column layout to center the login card on the screen
    _, main_col, _ = st.columns([1, 4, 1])

    with main_col:
        # We use nested columns inside the centered area
        col1, col2 = st.columns([1, 1], gap="large")

        # LEFT SIDE: Branding & Info
        with col1:
            st.image(
                "https://cdn-icons-png.flaticon.com/512/2964/2964514.png", 
                width=150
            )
            st.markdown("# FIT EVERYWHERE")
            st.markdown("### Your AI Powered Fitness Companion")
            st.write("Generate personalized workout plans based on:")
            
            st.markdown("""
            * **Age**
            * **Weight**
            * **Fitness Level**
            * **Equipment Availability**
            """)
            st.info("Stay consistent. Stay strong. 💪")

        # RIGHT SIDE: Input Form
        with col2:
            st.markdown("<h1 style='color:#ff5e62;'>Sign In</h1>", unsafe_allow_html=True)
            
            login_method = st.radio("Login via", ["Password", "OTP"], horizontal=True)
            email = st.text_input("Email Address", placeholder="name@example.com")

            if login_method == "Password":
                password = st.text_input("Password", type="password")
                if st.button("LOGIN"):
                    # Your existing logic
                    st.session_state.page = "dashboard"
                    st.rerun()

            else:
                # OTP Logic
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
                        token = create_jwt(email)
                        st.session_state.token = token
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
# UPDATED SIGNUP PAGE
# =====================================================
elif st.session_state.page == "signup":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h2 style='text-align:center'>CREATE ACCOUNT</h2>", unsafe_allow_html=True)
        
        # Step A: Collect Info
        with st.form("registration_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", 10, 80)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            email = st.text_input("Email Address")
            password = st.text_input("Create Password", type="password")
            goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Improve Cardio", "Flexibility"])
            
            if st.form_submit_button("Send Verification OTP"):
                if email and name and password:
                    otp = str(random.randint(100000, 999999))
                    st.session_state.generated_otp = otp
                    # Store data temporarily until verified
                    st.session_state.signup_temp_data = {
                        "name": name, "age": age, "gender": gender, 
                        "email": email, "password": password, "goal": goal
                    }
                    if send_otp_via_sendgrid(email, otp):
                        st.info(f"A verification code has been sent to {email}")
                    else:
                        st.error("Failed to send OTP. Check your configuration.")
                else:
                    st.warning("Please fill all fields before requesting OTP.")

        # Step B: Verify and Save
        st.markdown("---")
        verify_otp = st.text_input("Enter Verification OTP")
        if st.button("Verify & Complete Sign Up"):
            if verify_otp == st.session_state.get("generated_otp") and verify_otp != "":
                d = st.session_state.signup_temp_data
                try:
                    cursor.execute("INSERT INTO users (name, age, gender, email, password, goal) VALUES (?,?,?,?,?,?)",
                                   (d['name'], d['age'], d['gender'], d['email'], d['password'], d['goal']))
                    conn.commit()
                    st.success("Account Verified and Created! 🎉")
                    st.session_state.page = "login"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("This email is already registered.")
            else:
                st.error("Invalid OTP. Please try again.")

        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# =====================================================
# DASHBOARD
# =====================================================
elif st.session_state.page == "dashboard":
    import model  

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

    if st.button("Generate AI Workout Plan"):
        if not name:
            st.warning("Please enter your name first.")
        else:
            with st.spinner("🤖 AI is crafting your custom workout..."):
                # 1. Calculate BMI
                height_m = height / 100
                bmi = round(weight / (height_m**2), 2)
                bmi_status = "Normal" if 18.5 <= bmi <= 24.9 else "Overweight" # Simplified for logic

                # 2. Call the AI Model
                ai_response = model.generate_workout(name, age, goal, level, equipment, bmi_status)

                # 3. CRITICAL FIX: Save data for the View Plan page
                st.session_state.generated_plan = ai_response
                st.session_state.user_details = {"name": name, "goal": goal}
                
                # 4. Save to Database
                try:
                    cursor.execute(
                        "INSERT INTO workout_plans (email, goal, plan) VALUES (?, ?, ?)",
                        (st.session_state.get('email', 'Guest'), goal, ai_response)
                    )
                    conn.commit()
                except:
                    pass
                
                # 5. SWITCH PAGE
                st.session_state.page = "view_plan"
                st.rerun()

    st.markdown("---")
    if st.button("Logout"):
        if "token" in st.session_state:
            del st.session_state.token
        st.session_state.page = "login"
        st.rerun()               
# =====================================================
# VIEW PLAN PAGE (The "Nice UI" Page)
# =====================================================
elif st.session_state.page == "view_plan":
    # Custom Header for this page
    st.markdown(f"""
        <div style="background: linear-gradient(90deg,#ff9966,#ff5e62); padding: 40px; border-radius: 15px; text-align: center; color: white;">
            <h1 style="margin:0;">🔥 Your Personalized FitPlan</h1>
            <p style="opacity: 0.9;">Custom generated for {st.session_state.user_details['name']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") # Spacer

    col1, col2 = st.columns([2, 1])

    with col1:
        # Display the AI Plan inside a clean white card
        st.markdown("""
            <div style="background-color: white; padding: 30px; border-radius: 15px; border-left: 5px solid #ff5e62; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: #333;">📋 Workout Schedule</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Display the actual text from the model
        st.info(st.session_state.get('generated_plan', "No plan found."))

    with col2:
        # Side summary card
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #eee;">
                <h4>Summary</h4>
                <p><b>Goal:</b> {st.session_state.user_details['goal']}</p>
                <p><b>Status:</b> Active ✅</p>
                <hr>
                <p style="font-size: 0.8rem; color: #666;">This plan was generated by FitPlan AI based on your unique biometric data.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("⬅️ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
            
        if st.button("Logout"):
            del st.session_state.token
            st.session_state.page = "login"
            st.rerun()