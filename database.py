import sqlite3

# ----------------------------------

# CREATE CONNECTION (HUGGING FACE SAFE)

# ----------------------------------

def get_connection():
return sqlite3.connect("fitplan.db", check_same_thread=False)

# ----------------------------------

# INITIALIZE DATABASE

# ----------------------------------

def init_db():

```
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
```

# ----------------------------------

# ADD USER

# ----------------------------------

def add_user(name, age, gender, email, password, goal):

```
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
```

# ----------------------------------

# VERIFY USER

# ----------------------------------

def verify_user(email, password):

```
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM users WHERE email=? AND password=?",
    (email, password)
)

user = cursor.fetchone()
conn.close()

return user
```

# ----------------------------------

# ⭐ AUTO LOAD PROFILE (IMPORTANT)

# ----------------------------------

def get_user_profile(email):

```
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT name, age, gender, goal FROM users WHERE email=?",
    (email,)
)

data = cursor.fetchone()
conn.close()

return data
```

# ----------------------------------

# UPDATE PROFILE (VERY IMPORTANT FEATURE)

# ----------------------------------

def update_profile(name, age, gender, goal, email):

```
conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
UPDATE users
SET name=?, age=?, gender=?, goal=?
WHERE email=?
""",(name, age, gender, goal, email))

conn.commit()
conn.close()
```

# ----------------------------------

# SAVE WORKOUT PLAN

# ----------------------------------

def save_workout(email, goal, plan):

```
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
```

# ----------------------------------

# GET WORKOUT PLAN (NEW FEATURE)

# ----------------------------------

def get_workout(email):

```
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT goal, plan FROM workout_plans WHERE email=?",
    (email,)
)

data = cursor.fetchone()
conn.close()

return data
```

# ----------------------------------

# SAVE WEIGHT

# ----------------------------------

def save_weight(email, weight, date):

```
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO weights VALUES (?,?,?)",
    (email, weight, date)
)

conn.commit()
conn.close()
```

# ----------------------------------

# GET WEIGHT HISTORY

# ----------------------------------

def get_weights(email):

```
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT date, weight FROM weights WHERE email=? ORDER BY date",
    (email,)
)

data = cursor.fetchall()
conn.close()

return data
```
