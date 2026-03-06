import random
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret")

# Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Create JWT Token
def create_jwt(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Verify JWT
def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except:
        return None