import sqlite3
import functools
import logging
from typing import cast, Any, Callable, TypeVar, Optional, Dict, Sequence, Tuple
from pathlib import Path
from datetime import datetime

# -------------------------------
# Configure logger
# -------------------------------

today_str = datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path("logs") / today_str
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "cache_queries.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


# ------------------------
# Typing aliases
# ------------------------
Row = Tuple[Any, ...]  # single DB row as tuple
QueryResult = Sequence[Row]  # e.g., what cursor.fetchall() returns
F = TypeVar("F", bound=Callable[..., Any])  # generic for decorator typing

# ------------------------
# In-memory cache
# ------------------------
# Key: SQL query string, Value: QueryResult
query_cache: Dict[str, QueryResult] = {}


# -------------------------------
# Database Connection Decorator
# -------------------------------
def with_db_connection(func: F) -> F:
    """Decorator to manage SQLite database connection."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn: sqlite3.Connection | None = None
        try:
            conn = sqlite3.connect("users.db")
            logger.info("Database connection established.")
            return func(conn, *args, **kwargs)
        finally:
            if conn is not None:
                conn.close()
                logger.info("Database connection closed.")

    return cast(F, wrapper)


# -------------------------------
# Query Caching Decorator
# -------------------------------
def cache_query(func: F) -> F:
    """Decorator to cache database query results based on the SQL query string."""

    @functools.wraps(func)
    def wrapper(conn: sqlite3.Connection, query: str, *args, **kwargs) -> QueryResult:
        if query in query_cache:
            i = "⚡"
            logger.info("%s Cache hit for query: %s", i, query)
            return query_cache[query]

        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        i = "🗄️"
        logger.info("%s  Cache miss — query executed and cached: %s", i, query)

        # store a shallow immutable copy (tuple of rows) to avoid accidental mutation
        try:
            # convert to tuple for immutability, but keep row tuples as-is
            cached: QueryResult = tuple(result)  # type: ignore[assignment]
        except Exception:
            # fallback: store whatever was returned
            cached = result

        query_cache[query] = cached
        return cached

    return cast(F, wrapper)


# -------------------------------
# Function
# -------------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(
    conn: Optional[sqlite3.Connection] = None, query: str = ""
) -> Optional[QueryResult]:
    """Fetch users using a SQL query with caching enabled."""
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows: QueryResult = cursor.fetchall()
        return rows


# -------------------------------
# Usage
# -------------------------------
if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")

    print(users_again)

# Sample Output
# 2025-11-09 02:10:55,200 [INFO] Database connection established.
# 2025-11-09 02:10:55,201 [INFO] 🗄️  Cache miss — query executed and cached: SELECT * FROM users
# 2025-11-09 02:10:55,201 [INFO] Database connection closed.
# 2025-11-09 02:10:55,202 [INFO] Database connection established.
# 2025-11-09 02:10:55,202 [INFO] ⚡ Cache hit for query: SELECT * FROM users
# 2025-11-09 02:10:55,202 [INFO] Database connection closed.
# ((1, 'Alice Johnson', 'Crawford_Cartwright@hotmail.com', '2025-11-08 18:59:14'), (2, 'Bob Smith', 'bob@example.com', '2025-11-08 18:59:14'), (3, 'Charlie Lee', 'charlie@example.com', '2025-11-08 18:59:14'))
