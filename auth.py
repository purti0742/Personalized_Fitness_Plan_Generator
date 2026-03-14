import random
import jwt
import datetime
import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


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

def send_otp_via_brevo(receiver_email, otp):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    email_content = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": receiver_email}],
        sender={"name": "FitPlan AI", "email": "purti0742@gmail.com"},
        subject="Your FitPlan AI OTP",
        html_content=f"<strong>Your verification code is: {otp}</strong>"
    )
    
    try:
        api_instance.send_transac_email(email_content)
        return True
    except ApiException as e:
        print(f"Brevo Error: {e}")
        return False