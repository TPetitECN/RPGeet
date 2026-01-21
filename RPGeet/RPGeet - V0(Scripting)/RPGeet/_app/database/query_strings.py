# Obsolete with SQLAlchemy migration
### ------ Core ------ ###
CREATE_USER = "INSERT INTO core.Users (username, password) VALUES (%s, %s)"
VERIFY_USER = "SELECT password FROM core.Users WHERE username = %s"
GET_USER_GAMES = """
    SELECT g.game_id, g.name, r.gamemaster 
    FROM core.Games g
    JOIN core.R_Game_User r ON g.game_id = r.game_id
    WHERE r.username = %s
"""

CREATE_GAME = "INSERT INTO core.Games (name, system_id, source_id) VALUES (%s, %s, %s) RETURNING game_id"
JOIN_GAME = "INSERT INTO core.R_Game_User (game_id, username, gamemaster) VALUES (%s, %s, %s)"
GET_GAME = "SELECT * FROM core.Games WHERE game_id = %s"

FETCH_R_GAME_USER = "SELECT r_game_user FROM core.R_Game_User WHERE game_id = %s AND username = %s"

NEW_CHARACTER = "INSERT INTO core.Characters (r_game_user, name) VALUES (%s, %s) RETURNING character_id"
GET_CHARACTER = "SELECT * FROM core.Characters WHERE character_id = %s"
GET_GAME_CHARACTERS = """
    SELECT c.character_id, c.name, u.username
    FROM core.Characters c
    JOIN core.R_Game_User u ON c.r_game_user = u.r_game_user
    WHERE u.game_id = %s
"""