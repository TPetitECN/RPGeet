# Database connection parameters - Naive implementation
# Read database connection parameters from a private db.pwd file
# with open("db.pwd", "r") as f:
#     file = f.readlines()

# DB_HOST = file[0].strip()
# DB_PORT = file[1].strip()
# DB_NAME = file[2].strip()
# DB_USER = file[3].strip()
# DB_PASS = file[4].strip()

# Database connection parameters - Secure implementation using environment variables
from _app import _config as config
import os
from dotenv import load_dotenv
load_dotenv(config.DB_ENV)
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

import psycopg2
def get_db_connection() -> psycopg2.extensions.connection:
    """
    Establish and return a connection to the PostgreSQL database.

    :return: psycopg2 connection object, containing the database connection information
    :rtype: psycopg2.extensions.connection
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

import hashlib
def hash_password(password: str) -> str:
    """
    Hash a password using MD5. A stronger hashing algorithm could be relevant if the application
    were to be deployed in a production environment. In that case, consider using bcrypt or Argon2, as well as 64 bits passwords.
    
    :param password: Password string to hash
    :type password: str
    :return: MD5 hashed password string
    :type: str
    """
    return hashlib.md5(password.encode()).hexdigest()

if __name__ == "__main__":
    # Test the database connection
    try:
        connection = get_db_connection()
        print("Database connection established successfully.")
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")