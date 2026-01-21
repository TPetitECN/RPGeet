from urllib.parse import urlparse
from flask import Flask, request, url_for, render_template, redirect, session, flash
import _app.database.db as db
import _app.game_logic.game_logic as game_logic
from _app._aux import login_required, set_session_and_connect, Response
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Secure secret key for sessions
# ==================
# LOGIN ROUTES
# ==================

@app.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """
    Handle user login.
    
    :return: Rendered template or redirect response
    :rtype: str | Response
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.verify_user(username, password):
            return set_session_and_connect(username)
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    """
    Handle user registration.
    
    :return: Rendered template or redirect response
    :rtype: str | Response
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.create_user(username, password):
            flash('Registration successful! Welcome to RPGeet, {}!'.format(username))
            return set_session_and_connect(username)
        else:
            flash('Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout() -> Response:
    """
    Handle user logout.

    :return: Redirect response to login page
    :rtype: Response
    """
    session.pop('username', None)
    return redirect(url_for('login'))

# ==================
# GAME ROUTES
# ==================

@app.route('/')
@app.route('/lobby')
@login_required
def lobby() -> str:
    """
    Display the user lobby with their games.
    
    :return: Rendered lobby template
    :rtype: str
    """
    games = db.get_user_games(session['username'])
    return render_template('lobby.html', games=games, username=session['username'])

@app.route('/game/create', methods=['POST'])
@login_required
def create_game():
    """
    Create a new game.
    
    :return: Redirect response
    :rtype: Response
    """
    name = request.form['name']
    # For now, hardcoding system_id and source_id as 1. 
    # TODO: Fetch these from DB or form
    system_id = 1 
    source_id = 1
    
    game_id = db.create_game(name, system_id, source_id)
    if game_id:
        # Creator is automatically the GM
        db.join_game(game_id, session['username'], gamemaster=True)
        return redirect(url_for('view_game', game_id=game_id))
    else:
        flash('Error creating game')
        return redirect(url_for('lobby'))

@app.route('/game/<int:game_id>/join', methods=['POST'])
@login_required
def join_game(game_id : int) -> Response:
    """""
    Join a specific game.

    :param game_id: The ID of the game to join
    :type game_id: int

    :return: Rendered game template or redirect response
    :rtype: str | Response
    """
    # TODO: Check if game is joinable (e.g., not full, exists, etc.) ; Add invitations
    if db.join_game(game_id, session['username']):
        return redirect(url_for('view_game', game_id=game_id))
    else:
        flash('Could not join game')
        return redirect(url_for('lobby'))

@app.route('/game/<int:game_id>/delete', methods=['POST'])
@login_required
def delete_game(game_id : int) -> Response:
    # TODO: Implement delete logic (check if user is GM)
    return redirect(url_for('lobby'))

# ==================
# CHARACTER ROUTES
# ==================

@app.route('/characters')
@login_required
def characters() -> str:
    """""
    List all characters for the current user.

    :return: Rendered characters template
    :rtype: str
    """
    # TODO: Implement character listing
    return render_template('characters.html')

@app.route('/game/<int:game_id>')
@login_required
def view_game(game_id : int) -> str:
    """
    View a specific game.

    :param game_id: The ID of the game to view
    :type game_id: int

    :return: Rendered game template
    :rtype: str
    """
    game = db.get_game(game_id)
    characters = db.get_game_characters(game_id)
    return render_template('game.html', game=game, characters=characters, username=session['username'])

@app.route('/game/<int:game_id>/character/create', methods=['POST'])
@login_required
def create_character(game_id : int) -> Response:
    name = request.form['name']
    character_id = db.create_character(game_id, session['username'], name)
    if character_id:
        return redirect(url_for('view_game', game_id=game_id))
    else:
        flash('Error creating character')
        return redirect(url_for('view_game', game_id=game_id))

@app.route('/game/<int:game_id>/character/<int:character_id>')
@login_required
def view_character(game_id : int, character_id : int) -> str | tuple:
    character = db.get_character(character_id)
    if not character:
        return "Character not found", 404
        
    stats = game_logic.calculate_stats(character)
    return render_template('character.html', stats=stats, game_id=game_id)

@app.route('/game/<int:game_id>/character/<int:character_id>/edit', methods=['POST'])
@login_required
def edit_character(game_id : int, character_id : int) -> Response:
    """
    Edit a character in a game.
    
    :param game_id: The ID of the game
    :type game_id: int
    :param character_id: The ID of the character to edit
    :type character_id: int
    :return: Redirect response to the character view
    :rtype: Response
    """
    # TODO: Implement edit logic
    return redirect(url_for('view_character', game_id=game_id, character_id=character_id))

@app.route('/game/<int:game_id>/character/<int:character_id>/delete', methods=['POST'])
@login_required
def delete_character(game_id : int, character_id : int) -> Response:
    """"
    Delete a character from a game.
    :param game_id: The ID of the game
    :type game_id: int
    :param character_id: The ID of the character to delete
    :type character_id: int
    :return: Redirect response to the game view
    :rtype: Response
    """
    # TODO: Implement delete logic
    return redirect(url_for('view_game', game_id=game_id))

# ==================
# COMBAT ROUTES
# ==================

@app.route('/game/<int:game_id>/combat')
@login_required
def combat(game_id):
    state = game_logic.get_combat_state(game_id)
    return render_template('combat.html', game_id=game_id, state=state)

@app.route('/game/<int:game_id>/combat/add', methods=['POST'])
@login_required
def combat_add(game_id):
    name = request.form['name']
    initiative = int(request.form['initiative'])
    game_logic.add_participant(game_id, name, initiative)
    return redirect(url_for('combat', game_id=game_id))

@app.route('/game/<int:game_id>/combat/next', methods=['POST'])
@login_required
def combat_next(game_id):
    game_logic.next_turn(game_id)
    return redirect(url_for('combat', game_id=game_id))

@app.route('/game/<int:game_id>/combat/effect', methods=['POST'])
@login_required
def combat_effect(game_id):
    participant = request.form['participant']
    effect = request.form['effect']
    duration = int(request.form['duration'])
    game_logic.add_effect(game_id, participant, effect, duration)
    return redirect(url_for('combat', game_id=game_id))

if __name__ == '__main__':
    app.run(debug=True)

