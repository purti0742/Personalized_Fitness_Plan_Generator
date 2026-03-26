import sqlite3
import pandas as pd
import bcrypt

DB_NAME = "fitplan.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # USERS TABLE (Added food_pref and region)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            height REAL,
            email TEXT UNIQUE,
            password BLOB,
            goal TEXT,
            food_pref TEXT DEFAULT 'None',
            region TEXT DEFAULT 'None',
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
    # WATER INTAKE TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS water_intake(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            ml INTEGER,
            date TEXT
        )
    """)
    # CHALLENGES TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS challenges(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            title TEXT,
            start_date TEXT,
            duration_days INTEGER,
            status TEXT DEFAULT 'Active'
        )
    """)
    conn.commit()
    conn.close()

def add_user(name, age, gender, height, email, password, goal, food_pref='None', region='None'):
    try:
        conn = get_connection()
        cur = conn.cursor()
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cur.execute("""
            INSERT INTO users(name, age, gender, height, email, password, goal, food_pref, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, height, email, hashed_pw, goal, food_pref, region))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Add User Error:", e)
        return False

def verify_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    if user:
        stored_pw = user[6]
        if bcrypt.checkpw(password.encode(), stored_pw):
            return user
    return None

def get_user_profile(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, age, gender, height, goal, food_pref, region
        FROM users
        WHERE email=?
    """, (email,))
    data = cur.fetchone()
    conn.close()
    return data

def update_profile(name, age, gender, height, goal, food_pref, region, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET name=?, age=?, gender=?, height=?, goal=?, food_pref=?, region=?
        WHERE email=?
    """, (name, age, gender, height, goal, food_pref, region, email))
    conn.commit()
    conn.close()

def save_workout(email, focus, plan):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO workouts(email, focus, plan)
        VALUES (?, ?, ?)
    """, (email, focus, plan))
    conn.commit()
    conn.close()

def get_workouts(email):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT focus, plan, created_at FROM workouts WHERE email=? ORDER BY created_at DESC",
        conn,
        params=(email,)
    )
    conn.close()
    return df

def save_weight(email, weight, date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weights(email, weight, date)
        VALUES (?, ?, ?)
    """, (email, weight, date))
    conn.commit()
    conn.close()

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

def get_last_weight(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT weight FROM weights
        WHERE email=?
        ORDER BY date DESC LIMIT 1
    """, (email,))
    data = cur.fetchone()
    conn.close()
    if data:
        return data[0]
    return None

def save_water(email, ml, date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO water_intake(email, ml, date) VALUES (?, ?, ?)", (email, ml, date))
    conn.commit()
    conn.close()

def get_water_history(email):
    conn = get_connection()
    df = pd.read_sql_query("SELECT date, SUM(ml) as total_ml FROM water_intake WHERE email=? GROUP BY date", conn, params=(email,))
    conn.close()
    return df

def add_challenge(email, title, start_date, duration):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO challenges(email, title, start_date, duration_days) VALUES (?, ?, ?, ?)", (email, title, start_date, duration))
    conn.commit()
    conn.close()

def get_challenges(email):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM challenges WHERE email=?", conn, params=(email,))
    conn.close()
    return df
