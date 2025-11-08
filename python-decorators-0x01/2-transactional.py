#!/usr/bin/env python3
"""
Task 2: Transaction Management Decorator

This module implements a `transactional` decorator that ensures
database operations are executed within a transaction context.
If an exception occurs, the transaction is rolled back; otherwise, it is committed.
"""

import sqlite3
import functools
import logging
from typing import Any, Callable, TypeVar, Optional
from pathlib import Path
from datetime import datetime

# -------------------------------
# Configure logger
# -------------------------------

# Create logs directory if it doesn't exist
# Create a date-stamped folder name
today_str = datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path("logs") / today_str
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "transactions.log"

# Configure logging for visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

# Name logger
logger = logging.getLogger(__name__)

# Type hint for decorator
F = TypeVar("F", bound=Callable[..., Any])


# ----------------------------------
# Decorator: with_db_connection
# ----------------------------------
def with_db_connection(func: F) -> F:
    """
    Decorator to automatically open and close a database connection.

    The wrapped function must accept `conn` as its first argument.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            logging.info("Opened database connection to 'users.db'")
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logging.info("Closed database connection to 'users.db'")

    return wrapper  # type: ignore


# ----------------------------------
# Decorator: transactional
# ----------------------------------
def transactional(func: F) -> F:
    """
    Decorator to manage transactions.
    Commits if successful, rolls back on error.
    """

    @functools.wraps(func)
    def wrapper(conn: sqlite3.Connection, *args, **kwargs):
        try:
            logging.info(f"Starting transaction for {func.__name__}")
            result = func(conn, *args, **kwargs)
            conn.commit()
            logging.info(f"Transaction committed for {func.__name__}")
            return result
        except Exception as e:
            conn.rollback()
            logging.error(f"Transaction rolled back for {func.__name__} due to: {e}")
            raise

    return wrapper  # type: ignore


# ----------------------------------
# Example Usage
# ----------------------------------
@with_db_connection
@transactional
def update_user_email(
    conn: Optional[sqlite3.Connection] = None, user_id: int = 0, new_email: str = ""
):
    """Update a user's email address."""
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        logging.info(f"User {user_id} email updated to {new_email}")


if __name__ == "__main__":
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
    print("Email update completed successfully.")

# Output
# 2025-11-09 00:43:58,764 [INFO] Opened database connection to 'users.db'
# 2025-11-09 00:43:58,766 [INFO] Starting transaction for update_user_email
# 2025-11-09 00:43:58,778 [INFO] User 1 email updated to Crawford_Cartwright@hotmail.com
# 2025-11-09 00:43:58,788 [INFO] Transaction committed for update_user_email
# 2025-11-09 00:43:58,789 [INFO] Closed database connection to 'users.db'
# Email update completed successfully.
