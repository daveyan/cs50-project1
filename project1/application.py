import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from utils_sql import create_user_table
from utils_sql import create_password_table

from utils.user_utils import password_compare
from utils.user_utils import unique_user
from utils.user_utils import insert_user
from utils.user_utils import find_by_username

from utils.password_utils import insert_password
from utils.password_utils import get_password

from classes.user import User

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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/success", methods=["POST"])
def login_attempt():

    username = request.form.get("username")
    password = request.form.get("password")

    if ((not len(username)) or (not len(password))):
        return error_found("A field is empty")
    
    #find user
    user = find_by_username(db, username)
    if user is None:
         return error_found("Failed to login a ")
    
    #user is found
    found_password = get_password(db, user.id)
    
    if password is None:
        return error_found("Failed to login b")

    #password is found
    success = password_compare(password, found_password.password)

    if success:
        session["id"] = user.id
        val = session["id"]
        return render_template("welcome.html",username = user.username, firstname = user.firstname, lastname = user.lastname, sessionid = val)
    else: 
        return error_found("Failed to login c")



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

    user = User(username, firstname, lastname)

    create_user(db, user, password)

    return render_template("submit.html", 
    username=username, 
    firstname=firstname,
    lastname=lastname)

def error_found(message):
    return render_template("error.html", error=message)

def create_user(db, new_user, password):
    try:
        insert_user(db, new_user)
        user = find_by_username(db, new_user.username)
        insert_password(db, user.id, password)
    except Exception:
        print("ERROR CREATING USER")


    

