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
# BACKGROUND IMAGE (Online URL)
# -----------------------
bg_url = "https://cdn-uploads.huggingface.co/production/uploads/6989e9b496f31b77587e90e3/TQoDpBzWQcWXkKzBf3Fog.jpeg"

# -----------------------
# CUSTOM CSS
# -----------------------
st.markdown(f"""
<style>

/* Full Page Background */
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                      url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Remove default Streamlit padding */
.block-container {{
    padding-top: 0rem;
    padding-bottom: 0rem;
}}

/* Navbar */
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

/* Login Card */
.login-box {{
    width: 420px;
    margin: 120px auto;
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

/* Input Fields */
.stTextInput>div>div>input {{
    background-color: transparent;
    color: white;
    border: 1px solid #aaa;
    border-radius: 5px;
}}

/* Login Button */
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

/* Small Text */
.small-text {{
    margin-top: 15px;
    font-size: 14px;
    color: #ccc;
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
# LOGIN FORM
# -----------------------
st.markdown('<div class="login-box">', unsafe_allow_html=True)

st.markdown("<h2>PLEASE LOG IN</h2>", unsafe_allow_html=True)

email = st.text_input("Email Address")
password = st.text_input("Password", type="password")

if st.button("LOGIN"):
    if email and password:
        st.success("Login Successful ✅")
    else:
        st.error("Please enter Email and Password")

st.markdown('<div class="small-text">Don\'t have an account?</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)