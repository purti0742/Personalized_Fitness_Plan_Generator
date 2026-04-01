from pymongo import MongoClient
from datetime import datetime
import bcrypt

# ---------------- CONNECTION ----------------
MONGO_URI = "mongodb://localhost:27017/"   # change if using Atlas

client = MongoClient(MONGO_URI)
db = client["fitplan_ai"]

users_col = db["users"]
weights_col = db["weights"]
workouts_col = db["workouts"]


# ---------------- INIT DB ----------------
def init_db():
    # MongoDB creates collections automatically
    pass


# ---------------- PASSWORD HASH ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


# ---------------- USER FUNCTIONS ----------------
def add_user(name, age, gender, height, email, password, goal):
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
    weights_col.insert_one({
        "email": email,
        "weight": weight,
        "date": date
    })


def get_weights(email):
    data = list(weights_col.find({"email": email}).sort("date", 1))

    if not data:
        return None

    # Convert to format usable by Streamlit chart
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