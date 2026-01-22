from flask import Blueprint, request, url_for, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError
from app.models.core import db, Game, GameUser, Character, GameSources
import app.game_logic.game_logic as game_logic
from app.controllers._aux import login_required, Response, character_owner_or_gm_required

character_bp = Blueprint('character', __name__)

# ==================
# CHARACTER ROUTES
# ==================

@character_bp.route('/characters')
@login_required
def characters() -> str:
    """""
    List all characters for the current user.

    :return: Rendered characters template
    :rtype: str
    """
    user_participations = GameUser.query.filter_by(username=session['username']).all()
    user_characters = []
    
    for participation in user_participations:
        game_name = participation.game.name
        game_id = participation.game.game_id
        for char in participation.characters:
            user_characters.append({
                'id': char.character_id,
                'name': char.name,
                'game_name': game_name,
                'game_id': game_id
            })
            
    return render_template('character/characters.html', characters=user_characters)

@character_bp.route('/game/<int:game_id>/character/create', methods=['POST'])
@login_required
def create_character(game_id : int) -> Response:
    name = request.form['name']
    
    # Get the user's participation ID in this game
    gu = GameUser.query.filter_by(game_id=game_id, username=session['username']).first()
    
    if gu:
        try:
            new_char = Character(id_game_user=gu.id_game_user, name=name)
            db.session.add(new_char)
            db.session.commit()
            return redirect(url_for('game.view_game', game_id=game_id))
        except Exception as e:
            db.session.rollback()
            flash('Error creating character')
    else:
        flash('You must join the game first')

    return redirect(url_for('game.view_game', game_id=game_id))

@character_bp.route('/game/<int:game_id>/character/<int:character_id>')
@character_owner_or_gm_required
def view_character(game_id : int, character_id : int) -> str | tuple:
    character = Character.query.get(character_id)
    if not character:
        return "Character not found", 404
        
    # Convert to dict for compatibility with dummy game logic
    char_dict = {
        'character_id': character.character_id,
        'name': character.name
    }
    
    # DEBUG: Direct dispatch attempt to verify data retrieval
    game = Game.query.get(game_id)
    stats = {}
    if game and game.system_id == 1:
        try:
            from app.game_logic import pathfinder1 as pf1
            stats = pf1.calculate_stats(character.character_id)
        except Exception as e:
            print(f"Error calling PF1 stats directly: {e}")
            stats = {'Error': str(e)}
    else:
        stats = game_logic.calculate_stats(char_dict, game_id=game_id)
        
    return render_template('character/character.html', stats=stats, game_id=game_id, character_id=character_id)

@character_bp.route('/game/<int:game_id>/character/<int:character_id>/save', methods=['POST'])
@character_owner_or_gm_required
def save_character(game_id : int, character_id : int) -> Response:
    success, message = game_logic.update_character(character_id, request.form, game_id=game_id)
    if success:
        flash('Character saved successfully', 'success')
    else:
        flash(f'Error saving character: {message}', 'error')
        
    return redirect(url_for('character.view_character', game_id=game_id, character_id=character_id))

@character_bp.route('/game/<int:game_id>/character/<int:character_id>/edit', methods=['POST'])
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
    return redirect(url_for('character.view_character', game_id=game_id, character_id=character_id))

@character_bp.route('/game/<int:game_id>/character/<int:character_id>/delete', methods=['POST'])
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
    return redirect(url_for('game.view_game', game_id=game_id))
