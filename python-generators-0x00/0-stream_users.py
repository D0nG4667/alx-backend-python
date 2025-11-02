"""
Generator that streams rows from the user_data table in the ALX_prodev database.

This script connects to the MySQL database and yields one row at a time,
demonstrating efficient memory usage when processing large datasets.
"""

import os
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from sql_credentials import get_sql_credentials

WD = os.path.dirname(os.path.abspath(__file__))


@contextmanager
def connect_to_prodev():
    """Context manager for connecting to the ALX_prodev MySQL database."""
    connection = None
    try:
        host, user, password, port, database = get_sql_credentials(WD)
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        yield connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        yield None
    finally:
        if connection and connection.is_connected():
            connection.close()


def stream_users():
    """
    Generator that yields rows from the user_data table one by one.

    Yields:
        tuple: A single row (user_id, name, email, age)
    """
    with connect_to_prodev() as connection:
        if not connection:
            return

        # Buffered cursor solves unread results
        cursor = connection.cursor(buffered=True)
        try:
            cursor.execute("SELECT user_id, name, email, age FROM user_data;")
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row
        finally:
            cursor.close()


if __name__ == "__main__":
    # Example usage: Stream first 5 users
    for i, user in enumerate(stream_users(), start=1):
        print(f"✅ {user}")
        if i == 5:
            break