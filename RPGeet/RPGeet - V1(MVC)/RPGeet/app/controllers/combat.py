from flask import Blueprint, request, url_for, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError
from app.models.core import db, Game, GameUser, Character, GameSources
import app.game_logic.game_logic as game_logic
from app.controllers._aux import login_required, Response, gm_required

combat_bp = Blueprint('combat', __name__)


# ==================
# COMBAT ROUTES
# ==================

@combat_bp.route('/game/<int:game_id>/combat')
@login_required
def combat(game_id):
    state = game_logic.get_combat_state(game_id)
    return render_template('combat.html', game_id=game_id, state=state)

@combat_bp.route('/game/<int:game_id>/combat/add', methods=['POST'])
@login_required
def combat_add(game_id):
    name = request.form['name']
    initiative = int(request.form['initiative'])
    game_logic.add_participant(game_id, name, initiative)
    return redirect(url_for('combat.combat', game_id=game_id))

@combat_bp.route('/game/<int:game_id>/combat/next', methods=['POST'])
@login_required
def combat_next(game_id):
    game_logic.next_turn(game_id)
    return redirect(url_for('combat.combat', game_id=game_id))

@combat_bp.route('/game/<int:game_id>/combat/effect', methods=['POST'])
@login_required
def combat_effect(game_id):
    participant = request.form['participant']
    effect = request.form['effect']
    duration = int(request.form['duration'])
    game_logic.add_effect(game_id, participant, effect, duration)
    return redirect(url_for('combat.combat', game_id=game_id))
