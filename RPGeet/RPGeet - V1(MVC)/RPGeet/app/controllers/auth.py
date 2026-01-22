from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app

from ..models import core
from ..models.core import db, User
from ._aux import set_session_and_connect, Response


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """
    Handle user login.
    
    :return: Rendered template or redirect response
    :rtype: str | Response
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, user = User.login(username, password)
        if success:
            return set_session_and_connect(username)
        else:
            flash('Invalid username or password')
            current_app.logger.error(f"Failed to login user {username}: {user}")
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    """
    Handle user registration.
    
    :return: Rendered template or redirect response
    :rtype: str | Response
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, user = User.register(username, password)
        if success:
            flash("Account created successfully! Welcomoe to RPGeet, {}!".format(username))
            return set_session_and_connect(username)
        else:
            flash("Error : this name may already be taken.")
            current_app.logger.error(f"Failed to register user {username}: {user}")

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout() -> Response:
    """
    Handle user logout.

    :return: Redirect response to login page
    :rtype: Response
    """
    session.pop('username', None)
    return redirect(url_for('auth.login'))