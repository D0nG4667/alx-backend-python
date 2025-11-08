#!/usr/bin/env python3
"""
Task 3: Retry Database Queries Decorator

Implements a retry_on_failure(retries=3, delay=2) decorator that automatically
retries database operations on transient errors. Integrated with the
@with_db_connection decorator for seamless connection handling.
"""

import time
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

LOG_FILE = LOG_DIR / "retry_queries.log"

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


# ------------------------------
# Decorator: with_db_connection
# ------------------------------
def with_db_connection(func: F) -> F:
    """
    Decorator to automatically open and close a SQLite database connection.

    The wrapped function must accept `conn` as its first parameter.
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


# ------------------------------
# Decorator: retry_on_failure
# ------------------------------
def retry_on_failure(retries: int = 3, delay: int = 2) -> Callable[[F], F]:
    """
    Decorator to retry a function call if it raises a transient exception.

    Args:
        retries (int): Number of times to retry the operation.
        delay (int): Delay in seconds between retries.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    logging.info(f"Attempt {attempt}/{retries} for {func.__name__}")
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    logging.warning(
                        f"Transient error on attempt {attempt} for {func.__name__}: {e}"
                    )
                    if attempt < retries:
                        logging.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logging.error(
                            f"Operation failed after {retries} retries: {func.__name__}"
                        )
                        raise

        return wrapper  # type: ignore

    return decorator


# ------------------------------
# Usage
# ------------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn: Optional[sqlite3.Connection] = None):
    """Fetch all users with retry logic on transient errors."""

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        logging.info(f"Fetched {len(users)} users successfully.")
        return users


if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)


# Sample output
# 2025-11-09 01:20:01,493 [INFO] Opened database connection to 'users.db'
# 2025-11-09 01:20:01,493 [INFO] Attempt 1/3 for fetch_users_with_retry
# 2025-11-09 01:20:01,495 [INFO] Fetched 3 users successfully.
# 2025-11-09 01:20:01,495 [INFO] Closed database connection to 'users.db'
# [(1, 'Alice Johnson', 'Crawford_Cartwright@hotmail.com', '2025-11-08 18:59:14'), (2, 'Bob Smith', 'bob@example.com', '2025-11-08 18:59:14'), (3, 'Charlie Lee', 'charlie@example.com', '2025-11-08 18:59:14')]
