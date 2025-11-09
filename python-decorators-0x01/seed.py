import os
import csv
import uuid
import sqlite3
from pathlib import Path
from sqlite3 import Error, Connection, IntegrityError

# -------------------------
# Database Connection Setup
# -------------------------

WD = os.path.dirname(os.path.abspath(__file__))
db = Path("users.db")


def connect_db(db: Path):
    """Connect to SQLite DB."""
    try:
        conn = sqlite3.connect(db)

        return conn
    except Error as err:
        print(f"❌ Error: {err}")
        return None


# -------------------------
# Table Setup
# -------------------------


def create_table(connection: Connection):
    """Create the users table if it does not exist."""
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL NOT NULL
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(table_creation_query)
        cursor.close()
        print("✅ Table users created successfully")
    except Error as err:
        print(f"❌ Failed creating table: {err}")


# -------------------------
# Data Insertion
# -------------------------


def insert_data(connection: Connection, csv_file: Path):
    """Insert data from CSV into users table, avoiding duplicates."""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = int(row["age"])
                try:
                    cursor.execute(
                        "INSERT INTO users (user_id, name, email, age) VALUES (?, ?, ?, ?)",
                        (user_id, name, email, age),
                    )
                except IntegrityError:
                    # Skip duplicate emails
                    continue
        connection.commit()
        cursor.close()
        print(f"✅ Data from {csv_file} inserted successfully")
    except Exception as err:
        print(f"❌ Error inserting data: {err}")


# Seed data

# -------------------------
# Generator for Streaming Rows
# -------------------------


def stream_rows(connection: Connection, batch_size: int = 100):
    """
    Generator to stream rows from users table efficiently.
    Yields rows in batches.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row
    cursor.close()


# -------------------------
# Usage
# -------------------------

if __name__ == "__main__":
    conn = connect_db(db)
    if conn:
        create_table(conn)
        insert_data(
            conn, Path(os.path.join(WD, "../python-generators-0x00/user_data.csv"))
        )

        print("✅ Streaming first 5 rows using generator:")
        row_gen = stream_rows(conn)
        for i, row in enumerate(row_gen):
            print(row)
            if i >= 4:
                break

        conn.close()
