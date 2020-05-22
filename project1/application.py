import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from utils_sql import create_user_table
from utils_sql import create_password_table

from utils.user_utils import password_compare
from utils.user_utils import unique_user

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    create_user_table(db)
    create_password_table(db)
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/submit", methods=["POST"])
def register_submit():

    username = request.form.get("username")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    password = request.form.get("password")
    password_confirm = request.form.get("passwordConfirm")

    if ((not len(username)) or 
    (not len(firstname)) or 
    (not len(lastname)) or 
    (not len(password)) or
    (not len(password_confirm))):
        return error_found("A field is empty")

    valid_username = unique_user(db,username)
    if valid_username is False:
        return error_found("Username already exists")

    valid_password = password_compare(password, password_confirm)
    if valid_password is False:
        return error_found("Passwords are not identical")

    return render_template("submit.html", 
    username=username, 
    firstname=firstname,
    lastname=lastname)

def error_found(message):
    return render_template("error.html", error=message)
