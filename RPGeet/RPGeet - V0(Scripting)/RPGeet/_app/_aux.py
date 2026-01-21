from flask import session, redirect, url_for, request
from urllib.parse import urlparse
from functools import wraps

from werkzeug.wrappers.response import Response

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Decorator to ensure that a user is logged in before accessing a route.
        """
        if "username" not in session:
            return redirect(url_for("login", next=request.path))
        return func(*args, **kwargs)
    return wrapper

def set_session_user(name : str):
    """
    Set the session username.
    
    :param name: Username to set in session
    :type name: str
    """
    session['username'] = name

def set_session_and_connect(name : str) -> Response:
    """
    Set session user and redirect to the next page or lobby.
    
    :param name: Username to set in session
    :type name: str
    :return: Redirect response
    :rtype: werkzeug.wrappers.response.Response
    """
    set_session_user(name)
    next_page = request.args.get('next')
    print("Next page:", next_page)
    if not next_page or urlparse(next_page).netloc != '':
        next_page = url_for('lobby')
    return redirect(next_page)
