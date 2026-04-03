import json
import os

FILE_PATH = "remember_user.json"

def save_email(email):
    try:
        with open(FILE_PATH, "w") as f:
            json.dump({"email": email}, f)
    except:
        pass

def load_email():
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as f:
                data = json.load(f)
                return data.get("email", "")
    except:
        pass
    return ""