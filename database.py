import sqlite3
import pandas as pd
import bcrypt

DB_NAME = "fitplan.db"


# ---------------- CONNECTION ----------------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ---------------- INIT DATABASE ----------------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            height REAL DEFAULT 170,
            email TEXT UNIQUE,
            password TEXT,
            goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # WORKOUT TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            focus TEXT,
            plan TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # WEIGHT TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weights(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            weight REAL,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- ADD USER ----------------
def add_user(name, age, gender, email, password, goal):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # HASH PASSWORD
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cur.execute("""
            INSERT INTO users(name, age, gender, email, password, goal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age, gender, email, hashed_pw, goal))

        conn.commit()
        conn.close()
        return True
    except:
        return False


# ---------------- VERIFY USER ----------------
def verify_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()

    conn.close()

    if user:
        stored_pw = user[6]  # password column index
        if bcrypt.checkpw(password.encode(), stored_pw):
            return user

    return None


# ---------------- GET PROFILE ----------------
def get_user_profile(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, age, gender, goal, height
        FROM users
        WHERE email=?
    """, (email,))

    data = cur.fetchone()
    conn.close()

    if data:
        return data[0], data[1], data[2], data[3]   # return SAME as old (for app.py compatibility)

    return None


# ---------------- UPDATE PROFILE ----------------
def update_profile(name, age, gender, goal, email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET name=?, age=?, gender=?, goal=?
        WHERE email=?
    """, (name, age, gender, goal, email))

    conn.commit()
    conn.close()


# ---------------- SAVE WORKOUT ----------------
def save_workout(email, focus, plan):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO workouts(email, focus, plan)
        VALUES (?, ?, ?)
    """, (email, focus, plan))

    conn.commit()
    conn.close()


# ---------------- SAVE WEIGHT ----------------
def save_weight(email, weight, date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO weights(email, weight, date)
        VALUES (?, ?, ?)
    """, (email, weight, date))

    conn.commit()
    conn.close()


# ---------------- GET WEIGHTS ----------------
def get_weights(email):
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT date, weight FROM weights WHERE email=? ORDER BY date",
        conn,
        params=(email,)
    )

    conn.close()

    if df.empty:
        return None

    df = df.set_index("date")
    return df