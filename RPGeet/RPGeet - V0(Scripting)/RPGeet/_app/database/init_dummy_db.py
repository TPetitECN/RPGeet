from . import db

def populate_dummy_data():
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    print("Populating dummy data...")
    try:
        # 1. N_Game_System
        print("Inserting Game System...")
        cur.execute("""
            INSERT INTO core.N_Game_System (name) 
            VALUES ('Dummy System') 
            RETURNING system_id
        """)
        system_id = cur.fetchone()[0] # type: ignore
        
        # 2. N_Sources
        print("Inserting Source...")
        cur.execute("""
            INSERT INTO core.N_Sources (name, system_id) 
            VALUES ('Dummy Book', %s) 
            RETURNING source_id
        """, (system_id,))
        source_id = cur.fetchone()[0] # type: ignore
        
        # 3. Users
        print("Inserting Users...")
        # Create a GM user and a Player user
        gm_pass = db.hash_password('gm_pwd')
        player_pass = db.hash_password('player_pwd')
        
        cur.execute("""
            INSERT INTO core.Users (username, password) 
            VALUES ('gm_user', %s)
            ON CONFLICT (username) DO NOTHING
        """, (gm_pass,))
        
        cur.execute("""
            INSERT INTO core.Users (username, password) 
            VALUES ('player_user', %s)
            ON CONFLICT (username) DO NOTHING
        """, (player_pass,))
        
        # 4. Games
        print("Inserting Game...")
        cur.execute("""
            INSERT INTO core.Games (name, system_id, source_id) 
            VALUES ('Rise of the Runelords', %s, %s) 
            RETURNING game_id
        """, (system_id, source_id))
        game_id = cur.fetchone()[0] # type: ignore
        
        # 5. R_Game_User
        print("Linking Users to Game...")
        # GM
        cur.execute("""
            INSERT INTO core.R_Game_User (username, game_id, gamemaster) 
            VALUES ('gm_user', %s, TRUE)
        """, (game_id,))
        
        # Player
        cur.execute("""
            INSERT INTO core.R_Game_User (username, game_id, gamemaster) 
            VALUES ('player_user', %s, FALSE)
            RETURNING r_game_user
        """, (game_id,))
        player_r_id = cur.fetchone()[0] # type: ignore
        
        # 6. Characters
        print("Inserting Character...")
        cur.execute("""
            INSERT INTO core.Characters (r_game_user, name) 
            VALUES (%s, 'Valeros')
        """, (player_r_id,))
        
        conn.commit()
        print("Dummy data populated successfully!")
        print("Users created:")
        print(" - Username: gm_user, Password: password")
        print(" - Username: player_user, Password: password")
        
    except Exception as e:
        conn.rollback()
        print(f"Error populating data: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_dummy_data()
