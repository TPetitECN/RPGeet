import psycopg2
from psycopg2.extras import RealDictCursor

from .db_connect import get_db_connection, hash_password
from . import query_strings as queries

def create_user(username : str, password : str) -> bool:
    """
    Create a new user in the database.
    
    :param username: Username of the new user
    :type username: str
    :param password: Password (unhashed) of the new user
    :type password: str
    """
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cur.execute(queries.CREATE_USER, (username, hashed_pw))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def verify_user(username : str, password : str) -> bool:
    """
    Verify user credentials.
    
    :param username: Username to verify
    :type username: str
    :param password: Password (unhashed) to verify
    :type username: str
    :return: True if credentials are valid, False otherwise
    :rtype: bool
    """
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_pw = hash_password(password)
    cur.execute(queries.VERIFY_USER, (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user and user[0] == hashed_pw:
        return True
    return False

def get_user_games(username : str) -> list:
    """
    Retrieve games associated with a user.

    :param username: Username whose games to retrieve
    :type username: str
    :return: List of games
    :rtype: list
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(queries.GET_USER_GAMES, (username,))
    games = cur.fetchall()
    cur.close()
    conn.close()
    return games

def create_game(name : str, system_id : int, source_id : int) -> int:
    """
    Create a new game in the database.
    
    :param name: Name of the game
    :type name: str
    :param system_id: Game system identifier (D&D 5e, Pathfinder, etc.)
    :type system_id: int
    :param source_id: Source identifier (sourcebook, module, etc.)
    :type source_id: int
    :return: Game identifier
    :rtype: int
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(queries.CREATE_GAME, (name, system_id, source_id))
        game_id = cur.fetchone()[0] # type: ignore (only if insertion is successful)
        conn.commit()
        return game_id
    except Exception as e:
        conn.rollback()
        print(f"Error creating game: {e}")
        return -1
    finally:
        cur.close()
        conn.close()

def join_game(game_id : int, username : str, gamemaster : bool=False) -> bool:
    """
    Add a user to a game.
    
    :param game_id: Game identifier
    :type game_id: int
    :param username: Username of the user to add to the game
    :type username: str
    :param gamemaster: Whether the user is a gamemaster
    :type gamemaster: bool
    :return: True if successful, False otherwise
    :rtype: bool
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(queries.JOIN_GAME, (game_id, username, gamemaster))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def get_game(game_id : int) -> dict | None:
    #TODO: Return specific message/error if game not found.
    """
    Retrieve game details by game ID.

    :param game_id: Game identifier
    :type game_id: int
    :return: Game details as a dictionary or None if not found
    :rtype: dict[Any, Any] | None
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(queries.GET_GAME, (game_id,))
    game = cur.fetchone()
    cur.close()
    conn.close()
    return game

def create_character(game_id : int, username : str, name : str) -> int | None:
    """
    Create a new character for a user in a specific game.

    :param game_id: Game identifier
    :type game_id: int
    :param username: Username of the user
    :type username: str
    :param name: Name of the character
    :type name: str
    :return: Character identifier or None if creation failed
    :rtype: int | None
    """
    conn = get_db_connection()
    cur = conn.cursor()
    # First get the r_game_user id
    cur.execute(queries.FETCH_R_GAME_USER, (game_id, username))
    result = cur.fetchone()
    if not result:
        cur.close()
        conn.close()
        return None
    
    r_game_user_id = result[0]
    
    try:
        cur.execute(queries.NEW_CHARACTER, (r_game_user_id, name))
        character_id = cur.fetchone()[0] # type: ignore (only if insertion is successful)
        conn.commit()
        return character_id
    except Exception as e:
        conn.rollback()
        print(f"Error creating character: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_character(character_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(queries.GET_CHARACTER, (character_id,))
    character = cur.fetchone()
    cur.close()
    conn.close()
    return character

def get_game_characters(game_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(queries.GET_GAME_CHARACTERS, (game_id,))
    characters = cur.fetchall()
    cur.close()
    conn.close()
    return characters
