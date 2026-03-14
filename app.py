import streamlit as st
import random
import database as db
from auth import create_jwt, verify_jwt, send_otp_via_brevo
import model

# ---------------- INIT DB ----------------
db.init_db()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FitPlan AI",
    page_icon="💪",
    layout="wide"
)

# ---------------- GLASS THEME (YOUR SAME) ----------------
st.markdown("""
<style>
.stApp{
background: linear-gradient(135deg,#667eea,#764ba2);
color:white;
}
section.main > div{
background-color: transparent !important;
}
.block-container{
padding-top:2rem;
padding-left:5%;
padding-right:5%;
}
.login-card{
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
padding:40px;
border-radius:15px;
box-shadow:0px 8px 25px rgba(0,0,0,0.2);
color:white;
}
.stButton>button{
background:linear-gradient(45deg,#ff4b2b,#ff416c);
color:white;
border:none;
padding:10px 25px;
border-radius:8px;
font-weight:bold;
}
.stTextInput>div>div>input,
.stNumberInput>div>div>input{
border-radius:8px;
padding:10px;
background:rgba(255,255,255,0.25);
color:black;
border:1px solid rgba(255,255,255,0.4);
}
.stSelectbox>div>div{
background:rgba(255,255,255,0.25);
color:black;
border-radius:8px;
border:1px solid rgba(255,255,255,0.4);
}
[data-testid="stChart"]{
background:transparent;
}
.stTabs [data-baseweb="tab"]{
color:white;
font-size:16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATES ----------------
defaults = {
    "page": "login",
    "generated_otp": None,
    "user_email": None,
    "name": "",
    "age": 20,
    "gender": "Male",
    "goal": "Build Muscle",
    "height": 170,
    "weight": 70
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ================= LOGIN =================
if st.session_state.page == "login":

    _, main_col, _ = st.columns([1,3,1])

    with main_col:

        col1,col2 = st.columns([1,1])

        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=150)
            st.markdown("# FIT EVERYWHERE")
            st.markdown("### Your AI Powered Fitness Companion")

        with col2:

            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown("## Sign In")

            method = st.radio("Login via",["Password","OTP"],horizontal=True)
            email = st.text_input("Email")

            if method=="Password":

                password = st.text_input("Password",type="password")

                if st.button("LOGIN"):

                    user = db.verify_user(email,password)

                    if user:
                        st.session_state.user_email=email
                        st.session_state.token=create_jwt(email)

                        profile=db.get_user_profile(email)

                        if profile:
                            st.session_state.name=profile[0]
                            st.session_state.age=profile[1]
                            st.session_state.gender=profile[2]
                            st.session_state.goal=profile[3]

                        st.session_state.page="dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid Login")

            else:

                if st.button("Generate OTP"):
                    otp=str(random.randint(100000,999999))
                    st.session_state.generated_otp=otp
                    send_otp_via_brevo(email,otp)
                    st.success("OTP Sent")

                entered=st.text_input("Enter OTP")

                if st.button("Verify Login"):

                    if entered==st.session_state.generated_otp:

                        st.session_state.user_email=email
                        st.session_state.token=create_jwt(email)

                        profile=db.get_user_profile(email)

                        if profile:
                            st.session_state.name=profile[0]
                            st.session_state.age=profile[1]
                            st.session_state.gender=profile[2]
                            st.session_state.goal=profile[3]

                        st.session_state.page="dashboard"
                        st.rerun()
                    else:
                        st.error("Wrong OTP")

            if st.button("Create New Account"):
                st.session_state.page="signup"
                st.rerun()

            st.markdown('</div>',unsafe_allow_html=True)


# ================= SIGNUP =================
elif st.session_state.page=="signup":

    st.markdown("## Create Account")

    name=st.text_input("Full Name")
    age=st.number_input("Age",10,80)
    gender=st.selectbox("Gender",["Male","Female","Other"])
    email=st.text_input("Email")
    password=st.text_input("Password",type="password")
    goal=st.selectbox("Goal",["Build Muscle","Lose Weight","Improve Cardio"])

    if st.button("Register"):

        ok=db.add_user(name,age,gender,email,password,goal)

        if ok:
            st.success("Account Created")
            st.session_state.page="login"
            st.rerun()
        else:
            st.error("User Exists")

    if st.button("Back"):
        st.session_state.page="login"
        st.rerun()


# ================= DASHBOARD =================
elif st.session_state.page=="dashboard":

    st.title("🏋️ FitPlan AI Dashboard")

    tab1,tab2,tab3,tab4,tab5 = st.tabs(
        ["Dashboard","Profile","Workout","Weight","Logout"]
    )

    # DASHBOARD
    with tab1:
        st.subheader(f"Welcome {st.session_state.name} 👋")
        st.info(f"Logged in as {st.session_state.user_email}")

    # PROFILE
    with tab2:

        st.session_state.name = st.text_input(
            "Name",
            value=st.session_state.name
        )

        st.session_state.age = st.number_input(
            "Age",
            10,80,
            value=st.session_state.age
        )

        st.session_state.height = st.number_input(
            "Height",
            100,220,
            value=st.session_state.height
        )

        st.session_state.weight = st.number_input(
            "Weight",
            30,200,
            value=st.session_state.weight
        )

        if st.button("Update Profile"):

            db.update_profile(
                st.session_state.name,
                st.session_state.age,
                st.session_state.gender,
                st.session_state.goal,
                st.session_state.user_email
            )

            st.success("Profile Saved")

    # WORKOUT
    with tab3:

        goal=st.selectbox("Goal",
            ["Build Muscle","Lose Weight","Cardio"]
        )

        equipment=st.selectbox("Equipment",
            ["No Equipment","Dumbbells","Gym"]
        )

        level=st.selectbox("Level",
            ["Beginner","Intermediate","Advanced"]
        )

        if st.button("Generate Workout"):

            height_m=st.session_state.height/100
            bmi=round(st.session_state.weight/(height_m**2),2)

            bmi_status="Normal"
            if bmi>25:
                bmi_status="Overweight"

            plan=model.generate_workout(
                st.session_state.name,
                st.session_state.age,
                goal,
                level,
                equipment,
                bmi_status
            )

            st.success("Workout Generated")
            st.info(plan)

            db.save_workout(
                st.session_state.user_email,
                goal,
                plan
            )

    # WEIGHT
    with tab4:

        w=st.number_input("Today's Weight",30.0,200.0)

        if st.button("Save Weight"):
            db.save_weight(st.session_state.user_email,w,"today")
            st.success("Saved")

        data=db.get_weights(st.session_state.user_email)

        if data:
            st.line_chart(data)

    # LOGOUT
    with tab5:

        if st.button("Logout"):
            st.session_state.clear()
            st.session_state.page="login"
            st.rerun()