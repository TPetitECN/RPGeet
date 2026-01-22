from flask import session, redirect, url_for, request, abort
from urllib.parse import urlparse
from functools import wraps

from werkzeug.wrappers.response import Response

from app.models.core import User

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Decorator to ensure that a user is logged in before accessing a route.
        """
        if "username" not in session:
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        """
        Decorator to ensure that the user is an admin.
        """
        if not session.get('is_admin'): 
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function

def game_member_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        """
        Decorator to ensure that the user is a member of the specified game.
        """
        game_id = kwargs.get('game_id')
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user or not user.is_member_of_game(game_id):
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function

def character_owner_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        """
        Decorator to ensure that the user is the owner of the character.
        """
        character_id = kwargs.get('character_id')
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user or not user.is_owner_of_character(character_id):
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function

def gm_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        """
        Decorator to ensure that the user is the GM of the specified game.
        """
        game_id = kwargs.get('game_id')
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user or not user.is_gm_of_game(game_id):
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function

def character_owner_or_gm_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        """
        Decorator to ensure that the user is either the owner of the character or the GM of the game.
        """
        character_id = kwargs.get('character_id')
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user or not user.is_owner_or_gm_of_character(character_id):
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function

def set_session_and_connect(name : str) -> Response:
    """
    Set session user and redirect to the next page or lobby.
    
    :param name: Username to set in session
    :type name: str
    :return: Redirect response
    :rtype: werkzeug.wrappers.response.Response
    """
    user = User.query.filter_by(username=name).first()
    if user:
        user:User
        user.set_session_user()
    next_page = request.args.get('next')
    print("Next page:", next_page)
    if not next_page or urlparse(next_page).netloc != '':
        next_page = url_for('main.lobby')
    return redirect(next_page)
