from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import DBSetup, OpenConn
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, 
template_folder="./templates", # define the route for pages
)
app.secret_key = "secretkeyforapplication"

# For database 
DBSetup()


#for Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    with OpenConn() as conn:
        user = conn.execute("SELECT * FROM user_login WHERE id = ?", (user_id,)).fetchone()
        if user:
            return User(user['id'], user['username'])
    return None


class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)



@app.route('/')
def index():
    return render_template('index.html')

#SIGN UP ROUTE 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')    
    username = request.form.get('username')
    password = request.form.get('password')
    
    hashed_password = generate_password_hash(password)

    try:
        with OpenConn() as conn:
            conn.execute(
                "INSERT INTO user_login (username, password) VALUES (?, ?)",
                (username, hashed_password))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
    except sqlite3.IntegrityError:
            flash("Username already exists", "danger")
            return redirect(url_for('signup'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    with OpenConn() as conn:
        user = conn.execute(
            "SELECT * FROM user_login WHERE username = ?",
            (username,)
        ).fetchone()

    if user and check_password_hash(user['password'], password):
        user_check = User(user['id'], user['username'])
        login_user(user_check)
        flash("Logged in successfully!", "success")
        return redirect(url_for('index'))

    flash("Invalid username or password", "danger")
    return redirect(url_for('login'))

@app.route('/logout_post')
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('index'))

@app.route('/addPost', methods=["GET","POST"])
def add_post():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        if not title or not title.strip():
            flash("title is required, error")
            return render_template("addPost.html",title=title, description=description), 400
        if not description or not description.strip():
            flash("description is required, error")
            return render_template("addPost.html",title=title, description=description), 400
        
        with OpenConn() as conn:
            conn.execute(
                "INSERT INTO finalProjects (title, description) VALUES (?,?)",
                (title, description)
            )
            conn.commit()

            return redirect("/")
    return render_template("addPost.html")

if __name__ == '__main__':
    app.run(debug=True)