"""
seed.py - Python script to set up ALX_prodev database, create user_data table,
populate it from CSV, and stream rows using generators.
"""

import os
import mysql.connector
import csv
import uuid
from dotenv import load_dotenv

# -------------------------
# Database Connection Setup
# -------------------------

WD = os.path.dirname(os.path.abspath(__file__))


def get_sql_credentials():
    sql_env = load_dotenv(os.path.join(WD, '.env'))
    print(sql_env)
    host = os.getenv("HOST_DB")
    user = os.getenv("MYSQL_ROOT_USER")
    password = os.getenv("MYSQL_ROOT_PASSWORD")
    port = os.getenv("HOST_PORT")
    if not sql_env and not host:
        raise ValueError(
            "❌ .env file not found in the same folder as seep.py, or create env variables with HOST_DB, MYSQL_USER and MYSQL_ROOT_PASSWORD")
    return host, user, password, port


def connect_db(host=None, user=None, password=None, port=None):
    """Connect to MySQL server."""
    try:
        if host is None:
            host, user, password, port = get_sql_credentials()
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None


def create_database(connection, db_name="ALX_prodev"):
    """Create the database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        print(f"Database {db_name} is ready.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating database: {err}")


def connect_to_prodev(host=None, user=None, password=None, port=None, db_name="ALX_prodev"):
    """Connect to the ALX_prodev database."""
    try:
        if host is None:
            host, user, password, port = get_sql_credentials()

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None


# -------------------------
# Table Setup
# -------------------------

def create_table(connection):
    """Create the user_data table if it does not exist."""
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS user_data (
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
        print("✅ Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating table: {err}")


# -------------------------
# Data Insertion
# -------------------------

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table, avoiding duplicates."""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = int(row["age"])
                try:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
                except mysql.connector.IntegrityError:
                    # Skip duplicate emails
                    continue
        connection.commit()
        cursor.close()
        print(f"✅ Data from {csv_file} inserted successfully")
    except Exception as err:
        print(f"❌ Error inserting data: {err}")


# -------------------------
# Generator for Streaming Rows
# -------------------------

def stream_rows(connection, batch_size=100):
    """
    Generator to stream rows from user_data table efficiently.
    Yields rows in batches.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row
    cursor.close()


# -------------------------
# Example Usage
# -------------------------

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        insert_data(conn, os.path.join(WD, "./user_data.csv"))

        print("✅ Streaming first 5 rows using generator:")
        row_gen = stream_rows(conn)
        for i, row in enumerate(row_gen):
            print(row)
            if i >= 4:
                break

        conn.close()
