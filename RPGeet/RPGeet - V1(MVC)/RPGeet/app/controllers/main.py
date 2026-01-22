from flask import Blueprint, request, url_for, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError
from app.models.core import db, Game, GameUser, Character, GameSources
import app.game_logic.game_logic as game_logic
from app.controllers._aux import login_required, Response, character_owner_required, gm_required, game_member_required, character_owner_or_gm_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/lobby')
@login_required
def lobby() -> str:
    """
    Display the user lobby with their games.
    
    :return: Rendered lobby template
    :rtype: str
    """
    # Get all games the user is participating in
    participations = GameUser.query.filter_by(username=session['username']).all()
    
    # Format for template to match previous behavior
    games = []
    for p in participations:
        games.append({
            'game_id': p.game.game_id,
            'name': p.game.name,
            'gamemaster': p.gamemaster
        })
        
    return render_template('lobby.html', games=games, username=session['username'])
