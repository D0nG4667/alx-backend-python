"""
Task 1: Handle Database Connections with a Decorator

This module defines a decorator `with_db_connection` that automatically
handles opening and closing SQLite database connections for functions
that perform database operations.
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

LOG_FILE = LOG_DIR / "db_connection.log"

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


def with_db_connection(func: F) -> F:
    """
    Decorator to automatically open and close a database connection.

    The wrapped function must accept `conn` as its first argument.
    """

    # preserves the func runtime metadata (name, docstring, annotations)
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

    return wrapper  # type: ignore (needed because wrapper isn't strictly F)


@with_db_connection
def get_user_by_id(conn: Optional[sqlite3.Connection] = None, user_id: int = 0):
    """Fetch a user by ID."""

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()


# -------------------------------
# Usage
# -------------------------------
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
