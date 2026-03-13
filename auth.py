import random
import jwt
import datetime
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Call this once
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret")

# Create JWT Token
def create_jwt(email):
    # Updated to current standards
    payload = {
        "email": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Verify JWT
def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None

# Initialize the client once at the module level
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

def send_otp_via_sendgrid(receiver_email, otp):
    # 1. Define the from_email and the message content inside the function
    from_email = os.getenv("SENDGRID_FROM_EMAIL", "your-verified-sender@example.com")
    
    message = Mail(
        from_email=from_email,
        to_emails=receiver_email,
        subject='Your FitPlan AI OTP',
        html_content=f'<strong>Your verification code is: {otp}</strong>'
    )
    
    # 2. Perform the send action
    try:
        response = sg.send(message)
        # 202 is the success status code for SendGrid's API
        return response.status_code == 202
    except Exception as e:
        print(f"SendGrid Error: {e}")
        return False