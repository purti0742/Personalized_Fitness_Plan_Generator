import random
import jwt
import datetime
import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "fitplan_secret_2026")

def create_jwt(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24) # Extended for convenience
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def send_otp_via_brevo(receiver_email, otp):
    brevo_key = os.getenv('BREVO_API_KEY')
    sender_email = os.getenv("SENDER_EMAIL")
    
    if not brevo_key or not sender_email:
        print("Auth Error: Missing Brevo configuration.")
        return False
        
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = brevo_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    email_content = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": receiver_email}],
        sender={"name": "FitPlan AI", "email": sender_email},
        subject="Your FitPlan AI OTP",
        html_content=f"""
        <div style="font-family: sans-serif; padding: 20px; border: 1px solid #eee;">
            <h2>FitPlan AI Verification</h2>
            <p>Your verification code is: <strong style="font-size: 24px; color: #FF4D4D;">{otp}</strong></p>
            <p>This code will expire in 10 minutes.</p>
        </div>
        """
    )
    try:
        api_instance.send_transac_email(email_content)
        return True
    except ApiException as e:
        print(f"Brevo Error: {e}")
        return False
