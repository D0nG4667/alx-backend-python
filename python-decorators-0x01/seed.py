import sqlite3

# Connect to database (creates users.db if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Seed data
users = [
    ("Alice Johnson", "alice@example.com"),
    ("Bob Smith", "bob@example.com"),
    ("Charlie Lee", "charlie@example.com"),
]

cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)

conn.commit()
conn.close()
