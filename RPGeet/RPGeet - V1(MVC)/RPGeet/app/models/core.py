from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exists, and_

db = SQLAlchemy()

class GameSystem(db.Model):
    __tablename__ = 'n_game_system'
    __table_args__ = {'schema': 'core'}
    
    system_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    schema_name: Mapped[str] = mapped_column(nullable=False)

class Source(db.Model):
    __tablename__ = 'n_sources'
    __table_args__ = {'schema': 'core'}
    
    source_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    system_id: Mapped[int] = mapped_column(db.ForeignKey('core.n_game_system.system_id'), nullable=False)

class Game(db.Model):
    __tablename__ = 'games'
    __table_args__ = {'schema': 'core'}

    game_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    system_id: Mapped[int] = mapped_column(db.ForeignKey('core.n_game_system.system_id'), nullable=False)

    # Relationships
    participations = db.relationship('GameUser', back_populates='game')
    
class GameSources(db.Model):
    __tablename__ = 'r_game_sources'
    __table_args__ = {'schema': 'core'}

    id_game_source: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(db.ForeignKey('core.n_sources.source_id'), nullable=False)
    game_id: Mapped[int] = mapped_column(db.ForeignKey('core.games.game_id'), nullable=False)

class GameUser(db.Model):
    __tablename__ = 'r_game_user'
    __table_args__ = {'schema': 'core'}

    id_game_user: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.ForeignKey('core.users.username'), nullable=False)
    game_id: Mapped[int] = mapped_column(db.ForeignKey('core.games.game_id'), nullable=False)
    gamemaster: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relationships
    game = db.relationship('Game', back_populates='participations')
    user = db.relationship('User', back_populates='participations')
    characters = db.relationship('Character', back_populates='game_user')

class Character(db.Model):
    __tablename__ = 'characters'
    __table_args__ = {'schema': 'core'}

    character_id: Mapped[int] = mapped_column(primary_key=True)
    id_game_user: Mapped[int] = mapped_column(db.ForeignKey('core.r_game_user.id_game_user'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationships
    game_user = db.relationship('GameUser', back_populates='characters')

class User(db.Model):
    """
    Model representing a user from "users" table.
    
    Used for authentication.
    """
    __tablename__ = 'users'
    __table_args__ = {'schema': 'core'}
    
    username: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # Relationships
    participations = db.relationship('GameUser', back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    def set_session_user(self):
        """
        Set the session username.

        :param name: Username to set in session
        :type name: str
        """
        from flask import session
        session['username'] = self.username
        session['is_admin'] = self.admin
        
    def is_member_of_game(self, game_id : int) -> bool:
        """
        Check if the user is a member of the specified game.

        :param game_id: The ID of the game to check
        :type game_id: int
        :return: True if the user is a member of the game, False otherwise
        :rtype: bool
        """
        return db.session.query(exists().where(
            and_(GameUser.username == self.username, 
                 GameUser.game_id == game_id)
        )).scalar()
    
    def is_gm_of_game(self, game_id : int) -> bool:
        """
        Check if the user is the gamemaster of the specified game.

        :param game_id: The ID of the game to check
        :type game_id: int
        :return: True if the user is the gamemaster of the game, False otherwise
        :rtype: bool
        """
        return db.session.query(exists().where(
            and_(GameUser.username == self.username, 
                 GameUser.game_id == game_id, 
                 GameUser.gamemaster == True)
        )).scalar()
    
    def is_owner_of_character(self, character_id : int) -> bool:
        """
        Check if the user is the owner of the character.

        :param character_id: The ID of the character to check
        :type character_id: int
        :return: True if the user is the owner of the character, False otherwise
        :rtype: bool
        """
        return db.session.query(exists().where(
            and_(Character.character_id == character_id,
                 GameUser.id_game_user == Character.id_game_user,
                 GameUser.username == self.username)
        )).scalar()
    
    def is_owner_or_gm_of_character(self, character_id : int) -> bool:
        """
        Check if the user is either the owner of the character or the GM of the game.

        :param character_id: The ID of the character to check
        :type character_id: int
        :return: True if the user is the owner or GM, False otherwise
        :rtype: bool
        """
        if self.is_owner_of_character(character_id):
            return True
            
        game_id = db.session.query(GameUser.game_id).join(Character).filter(
            Character.character_id == character_id
        ).scalar()
        return self.is_gm_of_game(game_id) if game_id else False

    @classmethod
    def login(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            user:User
            if user.check_password(password):
                return True, user
            else:
                return False, "Invalid password"
        return False, "Invalid username"
    
    @classmethod
    def register(cls, username, password):
        # Test if user already exists
        if cls.query.filter_by(username=username).first():
            return False, "User already exists"
        
        try:
            # User creation attempt
            new_user = cls(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return True, new_user
        except IntegrityError:
            db.session.rollback() # ALWAYS rollback on exception
            return False, "Username already taken"
        except Exception as e:
            db.session.rollback()
            return False, f"Unexpected error: {e}"
        