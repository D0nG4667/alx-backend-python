import sqlite3
import functools
import logging
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

LOG_FILE = LOG_DIR / "query.log"

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),  # logs to console
    ],
)

logger = logging.getLogger(__name__)

# -------------------------------
# Decorator definition
# -------------------------------


def log_queries(func):
    """Decorator to log SQL queries using Python's logging system."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            logger.info(f"Executing SQL Query: {query}")
        else:
            logger.warning("No SQL query provided to function.")

        try:
            result = func(*args, **kwargs)
            logger.info("Query executed successfully.")
            return result
        except Exception as e:
            logger.exception(f"Error executing SQL query: {e}")
            raise

    return wrapper


# -------------------------------
# Function using decorator
# -------------------------------


@log_queries
def fetch_all_users(query):
    """Fetch all users from the users.db table."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# -------------------------------
# Usage
# -------------------------------
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)


# Output
# 2025-11-08 22:05:28,006 | INFO | Executing SQL Query: SELECT * FROM users
# 2025-11-08 22:05:28,012 | INFO | Query executed successfully.
# [(1, 'Alice Johnson', 'alice@example.com', '2025-11-08 18:59:14'), (2, 'Bob Smith', 'bob@example.com', '2025-11-08 18:59:14'), (3, 'Charlie Lee', 'charlie@example.com', '2025-11-08 18:59:14')]
