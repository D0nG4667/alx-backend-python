import os
from dotenv import load_dotenv


def get_sql_credentials(path: str):
    sql_env = load_dotenv(os.path.join(path, '.env'))
    host = os.getenv("HOST_DB")
    user = os.getenv("MYSQL_ROOT_USER")
    password = os.getenv("MYSQL_ROOT_PASSWORD")
    port = os.getenv("HOST_PORT")
    database = os.getenv("ALX_DB_NAME")
    if not sql_env and not host:
        raise ValueError(
            "❌ .env file not found in the same folder as seep.py, or create env variables with HOST_DB, MYSQL_USER and MYSQL_ROOT_PASSWORD")
    return host, user, password, port, database
