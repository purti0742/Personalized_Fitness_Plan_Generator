import sqlite3
import pandas as pd
import bcrypt

DB_NAME = "fitplan.db"


# ---------------- CONNECTION ----------------
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row   # enables column names
    return conn

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
            height REAL,
            email TEXT UNIQUE,
            password BLOB,
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

    # ✅ ADD INDEXES HERE
    cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_weights_email ON weights(email)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_workouts_email ON workouts(email)")

    conn.commit()
    conn.close()

# ---------------- ADD USER ----------------
def add_user(name, age, gender, height, email, password, goal):
    try:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO users(name, age, gender, height, email, password, goal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, age, gender, height, email, hashed_pw, goal))

            conn.commit()

        return True

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return False

# ---------------- VERIFY USER ----------------
def verify_user(email, password):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()

    if user:
        stored_pw = user["password"]
        if bcrypt.checkpw(password.encode(), stored_pw):
            return dict(user)

    return None


# ---------------- GET PROFILE ----------------
def get_user_profile(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, age, gender, height, goal
        FROM users
        WHERE email=?
    """, (email,))

    data = cur.fetchone()
    conn.close()

    return data


# ---------------- UPDATE PROFILE ----------------
def update_profile(name, age, gender, height, goal, email):
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            UPDATE users
            SET name=?, age=?, gender=?, height=?, goal=?
            WHERE email=?
        """, (name, age, gender, height, goal, email))

        conn.commit()


# ---------------- SAVE WORKOUT ----------------
def save_workout(email, focus, plan):
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO workouts(email, focus, plan)
            VALUES (?, ?, ?)
        """, (email, focus, plan))

        conn.commit()

# ---------------- GET WORKOUT HISTORY ----------------
def get_workouts(email):
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT focus, plan, created_at FROM workouts WHERE email=? ORDER BY created_at DESC",
        conn,
        params=(email,)
    )

    conn.close()
    return df


# ---------------- SAVE WEIGHT ----------------
def save_weight(email, weight, date):
    with get_connection() as conn:
        cur = conn.cursor()

        # Prevent duplicate same-day entry
        cur.execute("DELETE FROM weights WHERE email=? AND date=?", (email, date))

        cur.execute("""
            INSERT INTO weights(email, weight, date)
            VALUES (?, ?, ?)
        """, (email, weight, date))

        conn.commit()

# ---------------- GET WEIGHT HISTORY ----------------
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


# ---------------- GET LAST WEIGHT ----------------
def get_last_weight(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT weight FROM weights
        WHERE email=?
       ORDER BY datetime(date) DESC
    """, (email,))

    data = cur.fetchone()
    conn.close()

    if data:
        return data[0]

    return None
    