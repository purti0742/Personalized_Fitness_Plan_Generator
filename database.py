import sqlite3

def init_db():
    conn = sqlite3.connect("fitplan.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        name TEXT, age INTEGER, gender TEXT, email TEXT PRIMARY KEY, password TEXT, goal TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_plans(
        email TEXT, goal TEXT, plan TEXT
    )""")
    conn.commit()
    return conn

def add_user(name, age, gender, email, password, goal):
    conn = sqlite3.connect("fitplan.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", (name, age, gender, email, password, goal))
        conn.commit()
        return True
    except:
        return False

def save_workout(email, goal, plan):
    conn = sqlite3.connect("fitplan.db")
    cursor = conn.cursor()
    # This checks if a plan exists; if so, it replaces it. Otherwise, it inserts.
    cursor.execute("""
        INSERT INTO workout_plans (email, goal, plan) 
        VALUES (?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET goal=excluded.goal, plan=excluded.plan
    """, (email, goal, plan))
    conn.commit()
    conn.close()