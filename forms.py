from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class RegisterUser(FlaskForm):
    """Form for registering a new user."""

    username = StringField("Username:", 
            validators = [InputRequired(), Length(max=20)])#Unique(User.username),
    password = PasswordField("Password", 
            validators = [InputRequired()])
    email = StringField("Email:", 
            validators = [InputRequired(), Length(max=50)])
    first_name = StringField("First name:", 
            validators = [InputRequired(), Length(max=30)])
    last_name = StringField("Last name:", 
            validators = [InputRequired(), Length(max=30)])
            
class Login(FlaskForm):
    """Form for logging in"""
    
    username = StringField("Username:", 
            validators = [InputRequired(), Length(max=20)])#Unique(User.username),
    password = PasswordField("Password", 
            validators = [InputRequired()])
    
class CharacterForm(FlaskForm):
    """Submit new character"""
    
    name = StringField("Name:",
            validators = [InputRequired()])
    bio = TextAreaField("Bio:",
                validators = [InputRequired()])
    str_score = IntegerField("Strength Score:", 
                             validators=[NumberRange(min=1, max=30), InputRequired()])
    
class ItemForm(FlaskForm):
    """Form for adding Items"""
    
    name = StringField("Name:",
            validators = [InputRequired()])
    desc = TextAreaField("Description:",
                validators = [InputRequired()])
    weight = IntegerField("Weight (lbs):", 
                             validators=[InputRequired()])
    image_url = StringField("Image:")
    