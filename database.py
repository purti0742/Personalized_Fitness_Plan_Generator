import sqlite3

# ----------------------------------
# CREATE CONNECTION
# ----------------------------------
def get_connection():
    return sqlite3.connect("fitplan.db", check_same_thread=False)


# ----------------------------------
# INITIALIZE DATABASE
# ----------------------------------
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_plans(
        email TEXT PRIMARY KEY,
        goal TEXT,
        plan TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weights(
        email TEXT,
        weight REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


# ----------------------------------
# ADD USER (SIGNUP)
# ----------------------------------
def add_user(name, age, gender, email, password, goal):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users VALUES (?,?,?,?,?,?)",
            (name, age, gender, email, password, goal)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ----------------------------------
# VERIFY USER (LOGIN)
# ----------------------------------
def verify_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# ----------------------------------
# GET USER DETAILS (DISPLAY PROFILE)
# ----------------------------------
def get_user_details(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, age, gender, goal FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# ----------------------------------
# SAVE WORKOUT PLAN
# ----------------------------------
def save_workout(email, goal, plan):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO workout_plans(email, goal, plan)
    VALUES(?,?,?)
    ON CONFLICT(email) DO UPDATE SET
    goal=excluded.goal,
    plan=excluded.plan
    """, (email, goal, plan))

    conn.commit()
    conn.close()


# ----------------------------------
# SAVE WEIGHT
# ----------------------------------
def save_weight(email, weight, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO weights VALUES (?,?,?)",
        (email, weight, date)
    )

    conn.commit()
    conn.close()


# ----------------------------------
# GET WEIGHT HISTORY
# ----------------------------------
def get_weights(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT date, weight FROM weights WHERE email=? ORDER BY date",
        (email,)
    )

    data = cursor.fetchall()
    conn.close()

    return data