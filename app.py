from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import DBSetup, OpenConn
from flask_login import LoginManager

import sqlite3
import os
from werkzeug.security import generate_password_hash


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


app = Flask(__name__, 
template_folder="./templates", # define the route for pages
)
app.secret_key = "secretkeyforapplication"

# For database 
DBSetup()

@app.route('/')
def index():
    render_template('index.html')


@app.route('/signup', method=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
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

    return render_template('signup.html')

@app.route('/login', method=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
    if username.is_authenticated and password.is_authenthicated:
        return redirect(url_for('index'))
    

