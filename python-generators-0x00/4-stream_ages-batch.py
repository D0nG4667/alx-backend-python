"""
Module: Memory-Efficient Aggregation with Generators
Author: Your Name
Description: Compute average age of users from database without loading all rows into memory.
"""

from typing import cast, Generator,  List, Union
from decimal import Decimal
from seed import connect_to_prodev
from operator import itemgetter

# Types
AgeType = Union[int, float, Decimal]

# -------------------------------
# Generator to stream user ages
# -------------------------------


def stream_user_ages(batch_size: int = 100) -> Generator[list[AgeType], None, None]:
    """
    Yield user ages one by one from the database in batches.

    Args:
        batch_size: number of rows to fetch per batch
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection:
            cursor = connection.cursor()

            offset = 0
            while True:
                cursor.execute(
                    "SELECT age FROM user_data LIMIT %s OFFSET %s",
                    (batch_size, offset),
                )
                batch = cursor.fetchmany(batch_size)

                if not batch:
                    break

                # Efficiently extract ages in batch since there are a list of single values in tuple
                batch = list(map(itemgetter(0), batch))
                batch = cast(List[AgeType], batch)  # Telling the type checker

                yield batch
                offset += batch_size

    finally:
        if connection and cursor:
            cursor.close()
            connection.close()

# -------------------------------
# Function to calculate average age
# -------------------------------


def calculate_average_age(batch_size: int = 100) -> float:
    """
    Calculate average age of users using a generator.

    Args:
        batch_size: number of rows to fetch per batch

    Returns:
        Average age
    """
    total_age = 0
    count = 0
    for ages in stream_user_ages(batch_size):
        n = len(ages)
        ages_sum = sum(ages)
        total_age += int(ages_sum)
        count += n
    return total_age / count if count > 0 else 0.0


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    average_age = calculate_average_age(batch_size=10)
    print(f"Average age of users: {average_age:.2f}")
