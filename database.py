import sqlite3

DB_NAME = "fitplan.db"


# ---------- CONNECT ----------
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


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
        plan TEXT,
        created_at DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weights(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        weight REAL,
        created_at DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_workout_email ON workouts(email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_weight_email ON weights(email)")

    conn.commit()
    conn.close()


# ---------- ADD USER ----------
def add_user(name, age, gender, email, password, goal):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users(email,name,age,gender,password,goal)
        VALUES(?,?,?,?,?,?)
        """, (email, name, age, gender, password, goal))

        conn.commit()
        return True

    except Exception as e:
        print("DB ERROR:", e)
        return False

    finally:
        conn.close()


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

    profile = cursor.fetchone()

    conn.close()
    return profile


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


# ---------- GET WORKOUTS ----------
def get_workouts(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT goal, plan, created_at
    FROM workouts
    WHERE email=?
    ORDER BY id DESC
    """, (email,))

    data = cursor.fetchall()

    conn.close()
    return data


# ---------- SAVE WEIGHT ----------
def save_weight(email, weight):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO weights(email, weight)
    VALUES(?,?)
    """, (email, weight))

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