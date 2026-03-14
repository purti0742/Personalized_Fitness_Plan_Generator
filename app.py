import streamlit as st
import random
import database as db
from auth import create_jwt, verify_jwt, send_otp_via_brevo
import model

# -----------------------
# INITIALIZE DB
# -----------------------
db.init_db()

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="FitPlan AI",
    page_icon="💪",
    layout="wide"
)

# -----------------------
# MODERN UI CSS
# -----------------------
st.markdown("""
<style>

/* APP BACKGROUND */
.stApp{
background: linear-gradient(135deg,#667eea,#764ba2);
color:white;
}

/* REMOVE STREAMLIT DEFAULT WHITE BACKGROUND */
section.main > div{
background-color: transparent !important;
}

/* CONTAINER SPACING */
.block-container{
padding-top:2rem;
padding-left:5%;
padding-right:5%;
}

/* LOGIN CARD */
.login-card{
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
padding:40px;
border-radius:15px;
box-shadow:0px 8px 25px rgba(0,0,0,0.2);
color:white;
}

/* BUTTON STYLE */
.stButton>button{
background:linear-gradient(45deg,#ff4b2b,#ff416c);
color:white;
border:none;
padding:10px 25px;
border-radius:8px;
font-weight:bold;
}

/* BUTTON HOVER */
.stButton>button:hover{
transform:scale(1.05);
}

/* INPUT BOX FIX (GLASS STYLE) */
.stTextInput>div>div>input,
.stNumberInput>div>div>input{
border-radius:8px;
padding:10px;
background:rgba(255,255,255,0.25);  /* transparent glass */
color:black;                        /* visible text */
border:1px solid rgba(255,255,255,0.4);
}

/* PLACEHOLDER */
::placeholder{
color:#333;
}

/* SELECT BOX */
.stSelectbox>div>div{
background:rgba(255,255,255,0.25);
color:black;
border-radius:8px;
border:1px solid rgba(255,255,255,0.4);
}

/* REMOVE WHITE CHART BACKGROUND */
[data-testid="stChart"]{
background:transparent;
}

/* TABS */
.stTabs [data-baseweb="tab"]{
color:white;
font-size:16px;
}

</style>
""", unsafe_allow_html=True)
# -----------------------
# SESSION STATES
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

if "signup_temp_data" not in st.session_state:
    st.session_state.signup_temp_data = {}

if "user_email" not in st.session_state:
    st.session_state.user_email = None


# =====================================================
# LOGIN PAGE
# =====================================================
if st.session_state.page == "login":

    _, main_col, _ = st.columns([1,3,1])

    with main_col:

        col1,col2 = st.columns([1,1])

        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=150)
            st.markdown("# FIT EVERYWHERE")
            st.markdown("### Your AI Powered Fitness Companion")
            st.write("Generate personalized workout plans based on:")
            st.markdown("* Age\n* Weight\n* Fitness Level\n* Equipment")

        with col2:

            st.markdown('<div class="login-card">', unsafe_allow_html=True)

            st.markdown("## Sign In")

            login_method = st.radio("Login via",["Password","OTP"],horizontal=True)

            email = st.text_input("Email")

            if login_method == "Password":

                password = st.text_input("Password",type="password")

                if st.button("LOGIN"):

                    user = db.verify_user(email,password)

                    if user:
                        st.session_state.user_email=email
                        st.session_state.token=create_jwt(email)
                        st.session_state.page="dashboard"
                        st.rerun()

                    else:
                        st.error("Invalid login")

            else:

                if st.button("Generate OTP"):

                    otp=str(random.randint(100000,999999))
                    st.session_state.generated_otp=otp

                    if send_otp_via_brevo(email,otp):
                        st.success("OTP Sent")

                user_otp=st.text_input("Enter OTP")

                if st.button("Verify & Login"):

                    if user_otp==st.session_state.generated_otp:

                        st.session_state.user_email=email
                        st.session_state.token=create_jwt(email)
                        st.session_state.page="dashboard"
                        st.rerun()

                    else:
                        st.error("Invalid OTP")

            st.divider()

            if st.button("Create New Account"):
                st.session_state.page="signup"
                st.rerun()

            st.markdown("</div>",unsafe_allow_html=True)


# =====================================================
# SIGNUP PAGE
# =====================================================
elif st.session_state.page=="signup":

    col1,col2,col3=st.columns([1,2,1])

    with col2:

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown("## Create Account")

        name=st.text_input("Full Name")
        age=st.number_input("Age",10,80)
        gender=st.selectbox("Gender",["Male","Female","Other"])
        email=st.text_input("Email Address")
        password=st.text_input("Password",type="password")
        goal=st.selectbox("Goal",["Build Muscle","Lose Weight","Improve Cardio"])

        if st.button("Send OTP"):

            otp=str(random.randint(100000,999999))
            st.session_state.generated_otp=otp

            st.session_state.signup_temp_data={
                "name":name,
                "age":age,
                "gender":gender,
                "email":email,
                "password":password,
                "goal":goal
            }

            send_otp_via_brevo(email,otp)

            st.success("OTP Sent")

        verify=st.text_input("Enter OTP")

        if st.button("Verify & Signup"):

            if verify==st.session_state.generated_otp:

                d=st.session_state.signup_temp_data

                db.add_user(
                    d['name'],
                    d['age'],
                    d['gender'],
                    d['email'],
                    d['password'],
                    d['goal']
                )

                st.success("Account Created")

                st.session_state.page="login"
                st.rerun()

            else:
                st.error("Invalid OTP")

        if st.button("Back to Login"):
            st.session_state.page="login"
            st.rerun()

        st.markdown("</div>",unsafe_allow_html=True)


# =====================================================
# DASHBOARD
# =====================================================
elif st.session_state.page=="dashboard":

    st.title("🏋️ FitPlan AI Dashboard")

    tabs=st.tabs(["Dashboard","Profile","Workout Plan","Weight Tracker","Logout"])

    # DASHBOARD TAB
    with tabs[0]:

        st.subheader("Welcome")

        st.info(f"Logged in as {st.session_state.user_email}")

        c1,c2,c3=st.columns(3)

        with c1:
            st.metric("AI Workout Plans","Enabled")

        with c2:
            st.metric("Weight Tracking","Active")

        with c3:
            st.metric("Goal","Fitness Progress")


    # PROFILE TAB
    with tabs[1]:

        st.subheader("Profile")

        name=st.text_input("Name")
        age=st.number_input("Age",10,80)
        height=st.number_input("Height (cm)",100,220)
        weight=st.number_input("Weight (kg)",30,200)

        if st.button("Update Profile"):
            st.success("Profile Updated")


    # WORKOUT PLAN TAB
    with tabs[2]:

        st.subheader("Generate Workout Plan")

        goal=st.selectbox(
            "Goal",
            ["Build Muscle","Lose Weight","Improve Cardio","Flexibility"]
        )

        equipment=st.selectbox(
            "Equipment",
            ["No Equipment","Dumbbells","Gym Equipment"]
        )

        level=st.selectbox(
            "Fitness Level",
            ["Beginner","Intermediate","Advanced"]
        )

        if st.button("Generate AI Workout Plan"):

            height_m=height/100 if height>0 else 1.7

            bmi=round(weight/(height_m**2),2)

            bmi_status="Normal"

            if bmi>25:
                bmi_status="Overweight"

            plan=model.generate_workout(
                name,
                age,
                goal,
                level,
                equipment,
                bmi_status
            )

            st.success("Workout Plan Generated")

            st.info(plan)

            db.save_workout(
                st.session_state.user_email,
                goal,
                plan
            )


    # WEIGHT TRACKER
    with tabs[3]:

        st.subheader("Weight Tracker")

        today_weight=st.number_input("Enter today's weight",30.0,200.0)

        if st.button("Save Weight"):

            db.save_weight(
                st.session_state.user_email,
                today_weight,
                "today"
            )

            st.success("Weight Saved")

        st.subheader("Weight History")

        weights=db.get_weights(st.session_state.user_email)

        if weights:
            st.line_chart(weights)
        else:
            st.info("No weight records found")


    # LOGOUT
    with tabs[4]:

        if st.button("Logout"):

            st.session_state.clear()
            st.session_state.page="login"
            st.rerun()