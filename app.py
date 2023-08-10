"""Flask app for Capstone 1"""

from flask import Flask,render_template, redirect, flash, session, request, jsonify
from models import *
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenz"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def start():
    """Render landing page"""  
    return redirect("/register")
    
@app.route("/register", methods = ['GET', 'POST'])
def register():
    """Render registration form"""

    if session.get("username"): return redirect(f"/user/{session.get('username')}")
    register_form = RegisterUser()
    if register_form.validate_on_submit():
        if(User.query.get(register_form.username.data)):
            flash("That username is already taken")
            return redirect("/")
        new_user = User(username = register_form.username.data,
                      password = register_form.password.data,
                      email = register_form.email.data,
                      first_name = register_form.first_name.data,
                      last_name = register_form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        return redirect(f"/user/{new_user.username}") 
    return render_template("start.html",
        title = "Authentication",
        header = "Register User",
        form = register_form)
        
@app.route("/login", methods = ['GET', 'POST'])
def login():
    """Log user in, verifying that it is a valid username/password combo"""
    login_form = Login()
    if login_form.validate_on_submit():
        if User.authenticate(login_form.username.data, login_form.password.data):
            session["username"] = login_form.username.data
            return redirect(f"/user/{login_form.username.data}")
        flash("Invalid username or password")
        return redirect("/login")
    return render_template("login.html",
        title = "Authentication",
        header = "Login",
        form = login_form)
        
@app.route("/user/<username>")
def user(username):
    """Display user homepage with details and character"""
    if not session.get("username") == username:
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    return render_template("user.html",
        title = "Character List",
        header = f"{username}'s Characters",
        user = User.query.get(username),
        characters = Character.query.filter_by(username = username))
 
@app.route("/logout")
def logout():
    """Remove user from sesssion and return to the homescreen"""
    session.pop("username")
    return redirect("/")
    
@app.route("/users/<username>/character/add", methods = ['GET', 'POST'])
def add_character(username):
    """display and processs character page"""
    #ensure the user is logged in
    if not session.get("username") == username:
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    character_form = CharacterForm()
    if character_form.validate_on_submit():
        new_post = Character(name = character_form.name.data,
                            bio = character_form.bio.data,
                            str_score = character_form.str_score.data,
                            username = username)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/user/{username}")
    return render_template("add-character.html",
        title = "Authentication",
        header = "Character",
        form = character_form)
    
@app.route("/character/<character_id>/update", methods = ['GET', 'POST'])
def update_character(character_id):
    character = Character.query.get_or_404(character_id)
    #ensure the user is logged in
    if not session.get("username") == character.username:
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
        
    character_form = CharacterForm()
    if character_form.validate_on_submit():
        character.name = character_form.name.data
        character.bio = character_form.bio.data
        character.str_score = character_form.str_score.data
        db.session.commit()
        return redirect(f"/user/{character.username}")
        
    character_form.name.data = character.name
    character_form.bio.data = character.bio
    character_form.str_score.data = character.str_score
    return render_template("character.html",
        title = "Authentication",
        header = "Character",
        form = character_form)
    
@app.route("/character/<character_id>/delete")
def delete_character(character_id):
    character = Character.query.get_or_404(character_id)
    #ensure the user is logged in
    if not session.get("username") == character.username:
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    db.session.delete(character)
    db.session.commit() 
    return redirect(f"/user/{character.username}")