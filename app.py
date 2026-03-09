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
    # Use small gap to ensure panels touch
    _, center, _ = st.columns([1, 10, 1])
    with center:
        col1, col2 = st.columns([1, 1], gap="small")

        # LEFT SIDE
        with col1:
            st.markdown('<div class="left-panel">', unsafe_allow_html=True)
            st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=180)
            st.markdown('<div class="app-title">FIT EVERYWHERE</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="app-desc">
            Your <b>AI Powered Fitness Companion</b><br><br>
            Generate personalized workout plans based on:<br><br>
            • Age &nbsp;&nbsp; • Weight<br>
            • Fitness Level &nbsp;&nbsp; • Equipment Availability<br><br>
            Stay consistent. Stay strong. 💪
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # RIGHT SIDE
        with col2:
            st.markdown('<div class="right-panel">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">Sign In</div>', unsafe_allow_html=True)
            
            login_method = st.radio("Login via", ["Password", "OTP"], horizontal=True)
            email = st.text_input("Email Address")

            if login_method == "Password":
                password = st.text_input("Password", type="password")
                if st.button("LOGIN"):
                    st.session_state.page = "dashboard"
                    st.rerun()
            else:
                if st.button("Generate OTP"):
                    if email:
                        otp = str(random.randint(100000,999999))
                        st.session_state.generated_otp = otp
                        if send_otp_via_sendgrid(email, otp):
                            st.success("OTP sent!")
                        else:
                            st.error("Email failed.")
                    else:
                        st.warning("Enter email first.")

                user_otp = st.text_input("Enter OTP")
                if st.button("Verify & Login"):
                    if user_otp == st.session_state.get("generated_otp") and user_otp!="":
                        st.session_state.token = create_jwt(email)
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid OTP")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create New Account"):
                st.session_state.page = "signup"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# SIGNUP PAGE
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
    
    # ... Rest of your Dashboard Logic stays the same ...
    # (Simplified for display, but keep your original BMI logic here)
    
    if st.button("Logout"):
        del st.session_state.token
        st.session_state.page = "login"
        st.rerun()