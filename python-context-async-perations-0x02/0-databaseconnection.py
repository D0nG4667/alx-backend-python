"""
Implements a custom class-based context manager to handle opening
and closing SQLite database connections automatically.
"""

import sqlite3
import logging
import traceback
from sqlite3 import Connection, Cursor
from typing import Optional, Type
from pathlib import Path
from datetime import datetime

# -------------------------------
# Configure logger
# -------------------------------

today_str = datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path("logs") / today_str
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "db_connection.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


# -------------------------------------
# Class-based Context Manager
# -------------------------------------
class DatabaseConnection:
    """
    Context manager for managing SQLite database connections.

    Example:
        with DatabaseConnection("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.conn: Optional[Connection] = None

    def __enter__(self) -> Connection:
        """Establish and return the database connection."""
        self.conn = sqlite3.connect(self.db_name)
        logger.info(f"Opened connection to database: {self.db_name}")
        return self.conn

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb,
    ) -> None:
        """Close the database connection, handling exceptions gracefully."""
        if self.conn:
            if exc_type:
                self.conn.rollback()
                logger.error(
                    f"Transaction rolled back due to: {exc_type.__name__}: {exc_val}"
                )
                # Format the traceback into a readable string
                formatted_tb = "".join(traceback.format_tb(exc_tb))
                logger.error("Traceback:\n%s", formatted_tb)
            else:
                self.conn.commit()
                logger.info("Transaction committed successfully.")
            self.conn.close()
            logger.info(f"Closed connection to database: {self.db_name}")


# -------------------------------------
# Usage
# -------------------------------------
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor: Cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)

# Sample Output
# 2025-11-09 03:34:15,076 [INFO] Opened connection to database: users.db
# (1, 'Alice Johnson', 'Crawford_Cartwright@hotmail.com', '2025-11-08 18:59:14')
# (2, 'Bob Smith', 'bob@example.com', '2025-11-08 18:59:14')
# (3, 'Charlie Lee', 'charlie@example.com', '2025-11-08 18:59:14')
# 2025-11-09 03:34:15,078 [INFO] Transaction committed successfully.
# 2025-11-09 03:34:15,079 [INFO] Closed connection to database: users.db
