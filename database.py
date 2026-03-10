# -----------------------
# DATABASE CONNECTION
# -----------------------
conn = sqlite3.connect("fitplan.db", check_same_thread=False)
cursor = conn.cursor()

# Create Users Table
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

# Create Workout Plan Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS workout_plans(
    email TEXT,
    goal TEXT,
    plan TEXT
)
""")
conn.commit()


if st.form_submit_button("SIGN UP"):

    cursor.execute(
        "INSERT INTO users (name,age,gender,email,password,goal) VALUES (?,?,?,?,?,?)",
        (name,age,gender,email,password,goal)
    )

    conn.commit()

    st.success("Account Created Successfully! 🎉")


    if st.button("LOGIN"):

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
    )

    user = cursor.fetchone()

    if user:
        st.session_state.page = "dashboard"
        st.rerun()
    else:
        st.error("Invalid email or password")

        cursor.execute(
    "INSERT INTO workout_plans (email,goal,plan) VALUES (?,?,?)",
    (email,goal,generated_plan)
)

conn.commit()