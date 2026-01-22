from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
""" Base directory of the application. """

DB_ENV = BASE_DIR.parent / '.env'
""" Path to the .env file containing database environment variables. """

if __name__ == "__main__":
    print("Configuration loaded. BASE_DIR is set to:", BASE_DIR)