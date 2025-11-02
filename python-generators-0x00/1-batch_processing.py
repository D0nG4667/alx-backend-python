"""
Batch processing of large data from user_data table using Python generators.
"""

from typing import cast, Generator, Dict, List
from decimal import Decimal
from mysql.connector.types import RowItemType
from seed import connect_to_prodev  # Using existing DB connection function


def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, RowItemType]], None, None]:
    """
    Generator that fetches users in batches from the database.

    Args:
        batch_size (int): Number of rows to fetch per batch.

    Yields:
        sequence: Each batch of rows from user_data.
    """

    cursor = None
    connection = None
    try:
        connection = connect_to_prodev()
        # fetch as dict for clarity
        if connection:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM user_data", map_results=True)
            while True:
                batch = cursor.fetchmany(batch_size)
                # runtime check: fetchmany should return a list of dicts when dictionary=True
                assert isinstance(batch, list) and all(
                    isinstance(row, dict) for row in batch)

                batch = cast(List[Dict[str, RowItemType]],
                             batch)  # Telling the type checker
                if not batch:
                    break
                yield batch

    finally:
        if cursor and connection:
            cursor.close()
            connection.close()


def batch_processing(batch_size: int) -> Generator[Dict[str, RowItemType], None, None]:
    """
    Processes batches of users and filters users older than 25.

    Args:
        batch_size (int): Number of rows to fetch per batch.

    Yields:
        dict: User rows where age > 25. Age must be of type int, float or decimal
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            age: RowItemType = user.get("age")
            print(type(age))
            if age is not None and isinstance(age, (int, float, Decimal)) and int(age) > 25:
                yield user


# Example usage
if __name__ == "__main__":
    for user in batch_processing(batch_size=5):
        print(user)
