"""
Module: lazy pagination of users from database
Author: Gabriel Okundaye
Description: Demonstrates lazy-loading of paginated data from a MySQL database using a generator.
"""

from typing import cast, Generator, Dict, List, Optional
from mysql.connector.types import RowItemType
from seed import connect_to_prodev  # Using existing DB connection function

# -------------------------------
# Pagination helper
# -------------------------------

Row = Dict[str, RowItemType]
Rows = List[Row]


def paginate_users(page_size: int, offset: int) -> Optional[Rows]:
    """
    Fetch a page of users from the database.

    Args:
        page_size: number of records per page
        offset: starting point for the page

    Returns:
        List of user rows as dictionaries
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
            cursor.execute(query, (page_size, offset))
            rows = cursor.fetchall()
            # runtime check: fetchmany should return a list of dicts when dictionary=True
            assert isinstance(rows, list) and all(
                isinstance(row, dict) for row in rows)

            rows = cast(Rows, rows)  # Telling the type checker
            return rows
    finally:
        if connection and cursor:
            cursor.close()
            connection.close()

# -------------------------------
# Lazy pagination generator
# -------------------------------


def lazy_paginate(page_size: int) -> Generator[Rows, None, None]:
    """
    Lazily load paginated users using a generator.

    Args:
        page_size: Number of users per page

    Yields:
        Individual page dictionaries one by one
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# -------------------------------
# Example usage
# -------------------------------


if __name__ == "__main__":
    for page in lazy_paginate(page_size=5):
        for user in page:
            print(user)
