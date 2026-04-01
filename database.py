import os
import bcrypt
import certifi # Added to handle SSL handshake
from pymongo import MongoClient
from datetime import datetime

# ---------------- CONNECTION ----------------
# Use certifi.where() to provide the correct CA bundle for the SSL handshake
ca = certifi.where()

MONGO_URI = os.getenv("MONGO_URI") 

if not MONGO_URI:
    raise Exception("MONGO_URI not found. Please set it in Hugging Face Secrets.")

# Initialize the client with the TLS certificate fix
client = MongoClient(MONGO_URI, tlsCAFile=ca)

db = client["fitplan_ai"]

# Collections
users_col = db["users"]
weights_col = db["weights"]
workouts_col = db["workouts"]

# ---------------- PASSWORD HASH ----------------
def hash_password(password):
    # Ensure password is bytes for bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    # 'hashed' from MongoDB will be in bytes, which bcrypt needs
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# ---------------- USER FUNCTIONS ----------------
def add_user(name, age, gender, height, email, password, goal):
    # Check if user already exists
    if users_col.find_one({"email": email}):
        return False
    
    users_col.insert_one({
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "email": email,
        "password": hash_password(password),
        "goal": goal,
        "created_at": datetime.utcnow()
    })
    return True

def verify_user(email, password):
    user = users_col.find_one({"email": email})
    if user and check_password(password, user["password"]):
        return user
    return None

def get_user_profile(email):
    user = users_col.find_one({"email": email})
    if user:
        return (
            user.get("name"),
            user.get("age"),
            user.get("gender"),
            user.get("height"),
            user.get("goal")
        )
    return None

def update_profile(name, age, gender, height, goal, email):
    users_col.update_one(
        {"email": email},
        {"$set": {
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "goal": goal
        }}
    )

# ---------------- WEIGHT TRACKING ----------------
def save_weight(email, weight, date):
    # Tip: Ensure 'date' is a datetime object or a string ISO format
    weights_col.insert_one({
        "email": email,
        "weight": weight,
        "date": date
    })

def get_weights(email):
    data = list(weights_col.find({"email": email}).sort("date", 1))
    if not data:
        return None
    return {
        "date": [d["date"] for d in data],
        "weight": [d["weight"] for d in data]
    }

# ---------------- WORKOUTS ----------------
def save_workout(email, goal, plan):
    workouts_col.insert_one({
        "email": email,
        "goal": goal,
        "plan": plan,
        "created_at": datetime.utcnow()
    })