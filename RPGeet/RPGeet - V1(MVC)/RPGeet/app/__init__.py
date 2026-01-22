from flask import Flask
from app.models.core import db
from config import Config
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .controllers.main import main_bp
    app.register_blueprint(main_bp)
    
    from .controllers.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .controllers.game import game_bp
    app.register_blueprint(game_bp)

    from .controllers.character import character_bp
    app.register_blueprint(character_bp)
    
    from .controllers.combat import combat_bp
    app.register_blueprint(combat_bp)
    
    from .controllers.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))  # Test query to ensure DB connection
        except Exception as e:
            print(f"Database connection error: {e}")
            raise e
    print("App created and database connected successfully.")
    
    return app