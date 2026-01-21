from psycopg2 import IntegrityError
from _app import main
from _app.database.db_connect import get_db_connection, hash_password

app = main.app

if __name__ == '__main__':
    print('a')
    app.run(debug=True)
    print('b')
    
    # Test connexion to the database
    # from _app.database import db_connect
    # try:
    #     connection = db_connect.get_db_connection()
    #     print("Database connection established successfully.")
    #     connection.close() 
    # except Exception as e:
    #     print(f"Error connecting to the database: {e}")
    
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM core.N_game_systems")
    count = cur.fetchone()[0] # type: ignore
    print(f"Number of game systems in the database: {count}")
    if count == 0:
        print("No game systems found. Initializing the database with dummy data.")
        
        from _app.database.init_dummy_db import populate_dummy_data
        populate_dummy_data()
    cur.close()
    conn.close()