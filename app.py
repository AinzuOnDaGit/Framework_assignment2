from flask import Flask
from database import DBSetup, OpenConn
import sqlite3

app = Flask(
__name__,
template_folder="./templates", # define the route for pages
)
app.secret_key = "secretkeyforapplication"

@app.route("/")
def homepage():
    return "Hey"