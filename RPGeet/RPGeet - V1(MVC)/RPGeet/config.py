""" Configuration settings for the application.

Merges the previous _config.py and database/db_connect.py files into a single configuration module.
"""

from pathlib import Path
PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR / "_app"
""" Base directory of the application. """
DB_ENV = PROJECT_DIR / '.env'
""" Path to the .env file containing database environment variables. """

import os
from dotenv import load_dotenv
load_dotenv(DB_ENV)

class Config:
    """ Configuration class for Flask application settings.
    
    Example .env file (place in the root directory):
        SECRET_KEY=your_secret_key
        DEBUG=True
        DB_USER=your_db_user
        DB_PASS=your_db_password
        DB_HOST=localhost
        DB_PORT=5433
        DB_NAME=your_db_name
    """
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', '5433')  # Default port set to 5433
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable to save resources