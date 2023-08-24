"""Flask app for Capstone 1"""

from flask import Flask,render_template, redirect, flash, session, request, jsonify
from models import *
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenz"
#URI for local db instance
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/inventory_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mxtfbxxk:qrS4yMqEpnmPF0vyS_i-d3QxudEBfCOo@mahmud.db.elephantsql.com/mxtfbxxk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
#image API key:AIzaSyA2Rd8vOelYi-lpm7M0-uTemD69LYlS4ys
#custom search engine id:b74ccd7463d3745d4

connect_db(app)
db.create_all()

@app.route("/")
def start():
    """Render landing page"""  
    return redirect("/register")

def invalid_login(username):
    return session.get("username") != username
########################## USER AUTHENTICATION  ##################################
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
    return render_template("form.html",
        title = "Authentication",
        header = "Register User",
        form = register_form,
        button_label = "Register User")
        
@app.route("/login", methods = ['GET', 'POST'])
def login():
    """Log user in, verifying that it is a valid username/password combo"""
    #force a user to logout first before accessing the login page
    if session.get("username"): return redirect(f"/user/{session.get('username')}")

    login_form = Login()
    if login_form.validate_on_submit():
        if User.authenticate(login_form.username.data, login_form.password.data):
            session["username"] = login_form.username.data
            return redirect(f"/user/{login_form.username.data}")
        flash("Invalid username or password")
        return redirect("/login")
    return render_template("form.html",
        title = "Authentication",
        header = "Login",
        form = login_form,
        button_label = "Login")
        
@app.route("/user/<username>")
def user(username):
    """Display user homepage with details and character"""
    if invalid_login(username):
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    flash("Current session user is " + session.get("username"))
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
    
######################## CHARACTER CREATION AND EDITING ###########################
@app.route("/users/<username>/character/add", methods = ['GET', 'POST'])
def add_character(username):
    """display and processs character page"""
    #ensure the user is logged in
    if invalid_login(username):
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    character_form = CharacterForm()
    if character_form.validate_on_submit():
        new_post = Character(name = character_form.name.data,
                            bio = character_form.bio.data,
                            str_score = character_form.str_score.data,
                            image_url = character_form.image_url.data,
                            username = username)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/user/{username}")
    return render_template("form.html",
        title = "Create",
        header = "Character",
        form = character_form,
        button_label = "Create Character")
    
@app.route("/character/<character_id>/update", methods = ['GET', 'POST'])
def update_character(character_id):
    character = Character.query.get_or_404(character_id)
    #ensure the user is logged in
    if invalid_login(character.username):
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
        
    character_form = CharacterForm()
    if character_form.validate_on_submit():
        character.name = character_form.name.data
        character.bio = character_form.bio.data
        character.str_score = character_form.str_score.data
        character.image_url = character_form.image_url.data
        db.session.commit()
        return redirect(f"/user/{character.username}")
        
    character_form.name.data = character.name
    character_form.bio.data = character.bio
    character_form.str_score.data = character.str_score
    character_form.image_url.data = character.image_url
    return render_template("form.html",
        title = "Update",
        header = "Character",
        form = character_form,
        button_label = "Update Character")
    
@app.route("/character/<character_id>/delete")
def delete_character(character_id):
    character = Character.query.get_or_404(character_id)
    #ensure the user is logged in
    if invalid_login(character.username):
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    db.session.delete(character)
    db.session.commit() 
    return redirect(f"/user/{character.username}")


######################## ITEM CREATION AND EDITING ###########################
@app.route("/item")
def item_list():
    """Show all items currently in the system"""
    items = Item.query.order_by("name").all()
    return render_template("item/item.html",
        title = "All Items",
        header = "Item List",
        items = items)

@app.route("/item/add", methods = ['GET', 'POST'])
def item_add():
    """display and process item add page"""
    
    item_form = ItemForm()
    if item_form.validate_on_submit():
        new_item = Item(name = item_form.name.data,
                            desc = item_form.desc.data,
                            weight = item_form.weight.data,
                            image_url = item_form.image_url.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(f"/item")
    return render_template("item/add-item.html",
        title = "New Item",
        header = "Create Item",
        form = item_form)
    
@app.route("/item/<item_id>/update", methods = ['GET', 'POST'])
def update_item(item_id):
    """Update an item's details"""
    item = Item.query.get_or_404(item_id)
        
    item_form = ItemForm()
    if item_form.validate_on_submit():
        item.name = item_form.name.data
        item.desc = item_form.desc.data
        item.weight = item_form.weight.data
        item.image_url = item_form.image_url.data
        db.session.commit()
        return redirect("/item")
        
    item_form.name.data = item.name
    item_form.desc.data = item.desc
    item_form.weight.data = item.weight
    item_form.image_url.data = item.image_url
    return render_template("form.html",
        title = "Update",
        header = "Update Item",
        form = item_form,
        button_label = "Update Item")
    
@app.route("/item/<item_id>/delete")
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    db.session.delete(item)
    db.session.commit() 
    return redirect("/item")


######################## INVENTORY MANAGEMENT ###########################

@app.route("/character/<character_id>/inventory")
def character_inventory(character_id):
    """Display character's inventory"""

    character = Character.query.get_or_404(character_id)
    #ensure the user is logged in
    if invalid_login(character.username):
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    
    return render_template("inventory.html",
        title = "Inventory",
        header = "Inventory",
        character = character)

@app.route("/character/<character_id>/inventory/add", methods = ['GET', 'POST'])
def add_to_inventory(character_id):
    """Add an item to a character's inventory"""

    character = Character.query.get_or_404(character_id)
    #ensure the user is logged in
    if invalid_login(character.username):
        flash("Restricted page access attempted. Login first")
        return redirect("/login")
    
    #check to see if there is an item being submitted
    if request.args.get("added-item"):
        character.add_item(Item.query.get_or_404(request.args.get("added-item")))
        db.session.commit()
        return redirect(f"/character/{character.id}/inventory")
    
    return render_template("add-to-inventory.html",
        title = "Add",
        header = "Add Item",
        items = Item.query.order_by("name").all())
    
@app.route("/character/<character_id>/<item_id>/remove")
def remove_item(character_id, item_id):
    item = CharacterItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit() 
    return redirect(f"/character/{character_id}/inventory")