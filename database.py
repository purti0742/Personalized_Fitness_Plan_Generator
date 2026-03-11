import sqlite3

# -----------------------
# DATABASE INITIALIZATION
# -----------------------
def init_db():
    conn = sqlite3.connect("fitplan.db", check_same_thread=False)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        age INTEGER,
        gender TEXT,
        email TEXT PRIMARY KEY,
        password TEXT,
        goal TEXT
    )
    """)

    # Workout Plan Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_plans_v2(
        email TEXT PRIMARY KEY,
        goal TEXT,
        plan TEXT
    )
    """)

    # Weight Tracking Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weights(
        email TEXT,
        weight REAL,
        date TEXT
    )
    """)

    conn.commit()
    return conn


# -----------------------
# ADD NEW USER
# -----------------------
def add_user(name, age, gender, email, password, goal):
    conn = sqlite3.connect("fitplan.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users VALUES (?,?,?,?,?,?)",
            (name, age, gender, email, password, goal)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# -----------------------
# VERIFY LOGIN
# -----------------------
def verify_user(email, password):
    conn = sqlite3.connect("fitplan.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# -----------------------
# SAVE WORKOUT PLAN
# -----------------------
def save_workout(email, goal, plan):
    conn = sqlite3.connect("fitplan.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO workout_plans_v2 (email, goal, plan)
        VALUES (?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
        goal=excluded.goal,
        plan=excluded.plan
    """, (email, goal, plan))

    conn.commit()
    conn.close()


# -----------------------
# ADD WEIGHT ENTRY
# -----------------------
def add_weight(email, weight, date):
    conn = sqlite3.connect("fitplan.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO weights VALUES (?,?,?)",
        (email, weight, date)
    )

    conn.commit()
    conn.close()


# -----------------------
# GET WEIGHT HISTORY
# -----------------------
def get_weights(email):
    conn = sqlite3.connect("fitplan.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT date, weight FROM weights WHERE email=? ORDER BY date",
        (email,)
    )

    data = cursor.fetchall()
    conn.close()

    return data