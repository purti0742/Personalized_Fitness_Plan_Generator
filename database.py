import sqlite3

DB_NAME = "fitplan.db"


# ---------- CONNECT ----------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ---------- INIT TABLES ----------
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        email TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        password TEXT,
        goal TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        goal TEXT,
        plan TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weights(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        weight REAL,
        day TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------- ADD USER ----------
def add_user(name, age, gender, email, password, goal):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users VALUES(?,?,?,?,?,?)
        """, (email, name, age, gender, password, goal))

        conn.commit()
        conn.close()
        return True

    except:
        conn.close()
        return False


# ---------- VERIFY USER ----------
def verify_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user


# ---------- GET PROFILE ----------
def get_user_profile(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, age, gender, goal FROM users WHERE email=?
    """, (email,))

    data = cursor.fetchone()

    conn.close()

    return data


# ---------- UPDATE PROFILE ----------
def update_profile(name, age, gender, goal, email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET name=?, age=?, gender=?, goal=?
    WHERE email=?
    """, (name, age, gender, goal, email))

    conn.commit()
    conn.close()


# ---------- SAVE WORKOUT ----------
def save_workout(email, goal, plan):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO workouts(email, goal, plan)
    VALUES(?,?,?)
    """, (email, goal, plan))

    conn.commit()
    conn.close()


# ---------- SAVE WEIGHT ----------
def save_weight(email, weight, day="today"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO weights(email, weight, day)
    VALUES(?,?,?)
    """, (email, weight, day))

    conn.commit()
    conn.close()


# ---------- GET WEIGHTS ----------
def get_weights(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT weight FROM weights
    WHERE email=?
    ORDER BY id
    """, (email,))

    data = cursor.fetchall()

    conn.close()

    return [x[0] for x in data]
