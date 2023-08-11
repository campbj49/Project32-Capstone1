"""Models for Authentication app."""


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    app.app_context().push()
    
class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                   primary_key=True)
    password = db.Column(db.String(100),
                     nullable=False)
    email = db.Column(db.String(50),
                     nullable=False)
    first_name = db.Column(db.String(30),
                     nullable=False)
    last_name = db.Column(db.String(30),
                     nullable=False)
    
    #initialization extension method pulled from https://stackoverflow.com/questions/12701206/how-to-extend-python-class-init
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.password = bcrypt.generate_password_hash(self.password).decode("utf8")
        
    def authenticate(username, password):
        """Validate username and password, 
        returning user object if valid, false if not"""
        
        user = User.query.get(username)
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        
        else: return False
        
class Character(db.Model):
    """Character model"""

    __tablename__ = "characters"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20),
                        db.ForeignKey('users.username'))
    name = db.Column(db.String(100),
                   nullable = False)
    bio = db.Column(db.String, nullable= False)

    str_score = db.Column(db.Integer, nullable = False)
    
    user = db.relationship("User", backref="character")

class Item(db.Model):
    """Item model"""

    __tablename__ = "items"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(100),
                   nullable = False)
    desc = db.Column(db.String, nullable= False)

    #TODO: add some way to attach images, either through public htmls or an API id

    weight = db.Column(db.Integer, nullable = False)

    inventories = db.relationship("Character",
                                  secondary = "characters_items",
                                  backref = "items")
    
class CharacterItem(db.Model):
    """Inventory item model"""

    __tablename__ = "characters_items"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    character_id = db.Column(db.Integer,
                        db.ForeignKey('characters.id'))
    item_id = db.Column(db.Integer,
                        db.ForeignKey('items.id'))