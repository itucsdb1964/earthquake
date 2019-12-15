
from datetime import datetime

from flask import current_app, render_template, request, redirect, url_for, session, flash

from tables import database as d
from flask_session import Session


### convertTuple ###
import functools 
import operator  

#### login_page ###
#from passlib.apps import custom_app_context as hasher
from passlib.hash import pbkdf2_sha256

from forms import LoginForm
from user import get_user
from flask_login import LoginManager, login_user, logout_user

def convertTuple(tup): 
    str = functools.reduce(operator.add, (tup)) 
    return str

def add_earthquake_page():
    if request.method == "GET":
        return render_template("add_earthquake.html")
    else:
        form_agency = request.form["agency"]
        form_date_time = request.form["date_time"]
        form_latitude = request.form["latitude"]
        form_longitude = request.form["longitude"]

        print(form_agency)
        print(form_date_time)
        print(form_latitude)
        print(form_longitude)
        return redirect(url_for("add_earthquake_page"))

def add_comment_page():
    if request.method =="GET":
        return render_template("add_comment.html")
    else:
        form_id = request.form["id"]
        form_topic = request.form["topic"]
        form_comment = request.form["comment"]

        print(form_id)
        print(form_topic)
        print(form_comment)
        return redirect(url_for("add_comment_page"))

    
    
def earthquakes_page():
    db = current_app.config["db"]
    earths = db.get_earthquakes(0, 0)
    i = 0
    for earth in earths:
        earths[i] = list(earths[i])
        i = i + 1
    return render_template("earthquakes.html", earths = earths)

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def comments_page():
    db = current_app.config["db"]
    comments = db.get_comments()
    i = 0
    for comment in comments:
        comments[i] = list(comments[i])
        comments[i][0] = db.get_person(comment[0])[0][0]
        i = i + 1
    return render_template("comment.html", comments = comments)

def make_comment_page():   
    if request.method =="GET":
        return render_template("makecomment.html")
    else:
        topic = request.form["topic"]
        comment = request.form["comment"]
        print(comment)
        print(topic)
        name = session.get('user_id', 'not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        print(user_id[0])
        db.create_comment(topic, comment, user_id[0][0])
        #next_page = request.args.get("next", url_for("comments_page"))
        #render_template("makecomment.html")
        flash("Comment is succesfully sent :)")
        return redirect(url_for("make_comment_page"))
    
def signup_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = form.data["password"]
        next_page = request.args.get("next", url_for("login_page"))
        db = current_app.config["db"]
        db.create_person(username, pbkdf2_sha256.hash(password))
        flash("You signed up, you can enjoy our website now :)")
        return redirect(next_page)
    flash("Invalid credentials.")
    return render_template("signup.html", form=form)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if pbkdf2_sha256.verify(password, user.password[0][0] ):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)

def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

