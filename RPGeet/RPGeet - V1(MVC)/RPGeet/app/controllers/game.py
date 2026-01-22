from flask import Blueprint, request, url_for, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError
from app.models.core import db, Game, GameUser, Character, GameSources, GameSystem, Source
import app.game_logic.game_logic as game_logic
from app.controllers._aux import game_member_required, login_required, gm_required, Response
import json

game_bp = Blueprint('game', __name__)

@game_bp.route('/game/create', methods=['GET', 'POST'])
@login_required
def create_game():
    """
    Create a new game.
    
    :return: Redirect response
    :rtype: Response
    """
    
    def aux_load_systems_and_sources():
        """Load game systems and sources for the creation form."""
        systems = GameSystem.query.all()
        sources = Source.query.all()
        
        # Transform sources into a list of dicts for JS
        sources_data = [
            {"source_id": s.source_id, "name": s.name, "system_id": s.system_id} 
            for s in sources
        ]
        
        return systems, sources_data
    
    match request.method:
        case 'GET':
            try:
                systems, sources_data = aux_load_systems_and_sources()
        
                return render_template('game/create_game.html', 
                            systems=systems, 
                            sources_json=json.dumps(sources_data),
                            prev_name="",
                            prev_system=None)
            except Exception as e:
                flash('Error loading game creation form: {}'.format(str(e)))
                return redirect(url_for('main.lobby'))
        case 'POST':
            # Retrive form data
            name = request.form.get('name') # Game name
            system_id = request.form.get('system_id') # Selected game system ID
            selected_source_ids = request.form.getlist('source_ids') # List of selected source IDs
            
            try:
                # Create the game
                new_game = Game(name=name, system_id=system_id)
                db.session.add(new_game)
                db.session.flush()
                
                # Link selected sources to the game
                for sid in selected_source_ids:
                    link = GameSources(game_id=new_game.game_id, source_id=int(sid))
                    db.session.add(link)
                
                # Add the creator as gamemaster
                new_participation = GameUser(username=session['username'], game_id=new_game.game_id, gamemaster=True)
                db.session.add(new_participation)
                
                # Commit all changes
                db.session.commit()
            
                return redirect(url_for('game.view_game', game_id=new_game.game_id))
            except Exception as e:
                db.session.rollback()
                flash('Error creating game: {}'.format(str(e)))
                
                systems, sources_data = aux_load_systems_and_sources()
                return render_template('game/create_game.html',
                            systems=systems, 
                            sources_json=json.dumps(sources_data),
                            # Return the previous inputs
                            prev_name=name,
                            prev_system=system_id) 
            
        case _:
            flash("Invalid request method.")
            return redirect(url_for('main.lobby'))
        
@game_bp.route('/game/<int:game_id>/join', methods=['GET'])
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
    # Check if game exists
    game = Game.query.get(game_id)
    if not game:
        flash('Game not found')
        return redirect(url_for('main.lobby'))

    # Check if already joined
    if GameUser.query.filter_by(game_id=game_id, username=session['username']).first():
        return redirect(url_for('game.view_game', game_id=game_id))

    try:
        new_participation = GameUser(game_id=game_id, username=session['username'], gamemaster=False)
        db.session.add(new_participation)
        db.session.commit()
        return redirect(url_for('game.view_game', game_id=game_id))
    except Exception as e:
        db.session.rollback()
        flash('Could not join game')
        return redirect(url_for('main.lobby'))

@game_bp.route('/game/<int:game_id>')
@game_member_required
def view_game(game_id : int) -> str:
    """
    View a specific game.

    :param game_id: The ID of the game to view
    :type game_id: int

    :return: Rendered game template
    :rtype: str
    """
    game = Game.query.get(game_id)
    if not game:
        return "Game not found", 404

    # Get characters in the game
    # We join GameUser to get the username of the player
    char_rows = db.session.query(Character, GameUser).join(GameUser).filter(GameUser.game_id == game_id).all()
    
    characters = []
    for char, gu in char_rows:
        characters.append({
            'character_id': char.character_id,
            'name': char.name,
            'username': gu.username
        })
        
    return render_template('game/game.html', game=game, characters=characters, username=session['username'])

@game_bp.route('/game/<int:game_id>/delete', methods=['POST'])
@gm_required
def delete_game(game_id : int) -> Response:
    # TODO: Implement delete logic
    return redirect(url_for('main.lobby'))