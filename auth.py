import random
import jwt
import datetime
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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

load_dotenv()

def send_otp_via_sendgrid(receiver_email, otp):
    message = Mail(
        from_email='your-verified-sender@example.com', # Must match SendGrid settings
        to_emails=receiver_email,
        subject='Your FitPlan AI OTP',
        html_content=f'<strong>Your verification code is: {otp}</strong>'
    )
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response.status_code == 202 # 202 is the successful code
    except Exception as e:
        print(f"SendGrid Error: {e}")
        return False