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
        
class Feedback(db.Model):
    """Feedback model"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                   nullable = False)
    content = db.Column(db.String, nullable= False)
    username = db.Column(db.String(20),
                        db.ForeignKey('users.username'))
    
    user = db.relationship("User", backref="feedback")