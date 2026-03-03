import streamlit as st

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Fit Everywhere - Login",
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
    background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                      url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 0rem;
    padding-bottom: 0rem;
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    padding: 20px 60px;
    color: white;
    font-weight: 600;
    font-size: 18px;
}}

.nav-links a {{
    color: white;
    margin-left: 30px;
    text-decoration: none;
    font-size: 16px;
}}

.login-box {{
    width: 420px;
    margin: 100px auto;
    padding: 45px;
    background: rgba(0, 0, 0, 0.65);
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0px 0px 25px rgba(0,0,0,0.8);
}}

.login-box h2 {{
    margin-bottom: 30px;
    letter-spacing: 1px;
}}

.stTextInput>div>div>input {{
    background-color: transparent;
    color: white;
    border: 1px solid #aaa;
    border-radius: 5px;
}}

.stButton>button {{
    width: 100%;
    background-color: #e50914;
    color: white;
    border-radius: 6px;
    height: 45px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}}

.stButton>button:hover {{
    background-color: #ff1f2e;
    color: white;
}}

.small-text {{
    margin-top: 15px;
    font-size: 14px;
    color: #ccc;
    cursor: pointer;
}}

</style>
""", unsafe_allow_html=True)

# -----------------------
# NAVBAR
# -----------------------
st.markdown("""
<div class="navbar">
    <div>FIT EVERYWHERE</div>
    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">My Progress</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# SESSION STATE FOR TOGGLE
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# -----------------------
# LOGIN / SIGNUP BOX
# -----------------------
st.markdown('<div class="login-box">', unsafe_allow_html=True)

# ================= LOGIN =================
if st.session_state.page == "login":

    st.markdown("<h2> LOG IN</h2>", unsafe_allow_html=True)

    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if email and password:
            st.success("Login Successful ✅")
        else:
            st.error("Please enter Email and Password")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = "signup"
        st.rerun()

# ================= SIGNUP =================
elif st.session_state.page == "signup":

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
    
    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)