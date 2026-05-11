import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

# Add default user
cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ("admin", "1234"))

conn.commit()
conn.close()

print("Database created!")