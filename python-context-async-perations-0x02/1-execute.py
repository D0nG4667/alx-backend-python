"""
Implements a reusable class-based context manager `ExecuteQuery`
that manages database connections and executes parameterized queries.
"""

import sqlite3
import logging
import traceback
from sqlite3 import Connection, Cursor
from typing import Any, Optional, Sequence, Type, List, Tuple
from pathlib import Path
from datetime import datetime

# -------------------------------
# Configure logger
# -------------------------------

today_str = datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path("logs") / today_str
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "db_query.log"

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
# Reusable Context Manager Class
# -------------------------------------
class ExecuteQuery:
    """
    Context manager for executing SQL queries safely.

    Example:
        with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
            for row in results:
                print(row)
    """

    def __init__(
        self, db_name: str, query: str, params: Optional[Sequence[Any]] = None
    ) -> None:
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None
        self.results: List[Tuple[Any, ...]] = []

    def __enter__(self) -> List[Tuple[Any, ...]]:
        """Open the connection, execute the query, and return the results."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_name}")

            if self.params:
                self.cursor.execute(self.query, self.params)
            else:
                self.cursor.execute(self.query)

            self.results = self.cursor.fetchall()
            logger.info(f"Executed query: {self.query} | Params: {self.params}")
            return self.results

        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb,
    ) -> None:
        """Ensure proper cleanup and commit/rollback management."""
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
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        for row in results:
            print(row)
