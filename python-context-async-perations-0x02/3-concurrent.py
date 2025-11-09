"""
Run multiple SQLite queries concurrently using aiosqlite and asyncio.gather.

Requires:
    uv add aiosqlite

This script defines:
- async_fetch_users(): fetch all users
- async_fetch_older_users(): fetch users older than 40
- fetch_concurrently(): run both concurrently with asyncio.gather
"""

from __future__ import annotations

import asyncio
import logging
import aiosqlite
from pathlib import Path
from datetime import datetime
from typing import List
from aiosqlite import Row  # a single DB row (tuple of columns)

# -------------------------------
# Configure logger
# -------------------------------

today_str = datetime.now().strftime("%Y-%m-%d")
LOG_DIR = Path("logs") / today_str
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "concurrent.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


async def async_fetch_users(db_path: str = "users.db") -> List[Row]:
    """
    Asynchronously fetch all users from the database.
    Returns list of rows.
    """
    logger.info("Starting async_fetch_users")
    rows: List[Row] = []
    try:
        async with aiosqlite.connect(db_path) as db:
            # return rows as tuples (default)
            async with db.execute("SELECT * FROM users") as cursor:
                async for row in cursor:
                    rows.append(row)
    except Exception as exc:
        logger.exception("Error in async_fetch_users: %s", exc)
        raise
    logger.info("Completed async_fetch_users (rows=%d)", len(rows))
    return rows


async def async_fetch_older_users(
    min_age: int = 40, db_path: str = "users.db"
) -> List[Row]:
    """
    Asynchronously fetch users older than `min_age`.
    Returns list of rows.
    """
    logger.info("Starting async_fetch_older_users (min_age=%d)", min_age)
    rows: List[Row] = []
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute(
                "SELECT * FROM users WHERE age > ?", (min_age,)
            ) as cursor:
                async for row in cursor:
                    rows.append(row)
    except Exception as exc:
        logger.exception("Error in async_fetch_older_users: %s", exc)
        raise
    logger.info("Completed async_fetch_older_users (rows=%d)", len(rows))
    return rows


async def fetch_concurrently() -> None:
    """
    Run async_fetch_users and async_fetch_older_users concurrently and print results.
    """
    logger.info("Running queries concurrently with asyncio.gather")
    # run both coroutines concurrently
    users_task = async_fetch_users()
    older_users_task = async_fetch_older_users(min_age=40)

    try:
        users, older_users = await asyncio.gather(users_task, older_users_task)
    except Exception:
        logger.exception("One or more concurrent tasks failed")
        raise

    # Print summary and (optionally) a few rows for verification
    logger.info("Total users fetched: %d", len(users))
    logger.info("Users older than 40 fetched: %d", len(older_users))

    print("\n--- Sample: all users (first 5) ---")
    for r in users[:5]:
        print(r)

    print("\n--- Sample: users older than 40 (first 5) ---")
    for r in older_users[:5]:
        print(r)


if __name__ == "__main__":
    # Run the concurrent fetch
    asyncio.run(fetch_concurrently())
