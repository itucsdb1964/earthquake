from flask import Flask, session ,current_app, render_template, request, redirect, url_for, flash
from datetime import datetime

import views
from flask_session import Session

from flask_login import LoginManager, login_user, logout_user
from user import get_user

from tables import database as d 
#### login_page ###
#from passlib.apps import custom_app_context as hasher
from passlib.hash import pbkdf2_sha256
from forms import LoginForm

lm = LoginManager()


app = Flask(__name__)

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

    
app.config.from_object("settings")

@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

@app.route("/signup",methods=["GET", "POST"])
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

@app.route("/login",methods=["GET", "POST"])
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

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

@app.route("/makecomment",methods=["GET", "POST"])
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
        db.create_comment(topic, comment, user_id[0][0])
        #next_page = request.args.get("next", url_for("comments_page"))
        #render_template("makecomment.html")
        flash("Comment is succesfully sent :)")
        return redirect(url_for("make_comment_page"))

@app.route("/comments", methods=["GET","POST"])
def comments_page():
    db = current_app.config["db"]
    if request.method == "GET":
        comments = db.get_comments()
        i = 0
        for comment in comments:
            comments[i] = list(comments[i])
            comments[i][0] = db.get_person(comment[0])[0][0]
            i = i + 1
        return render_template("comment.html", comments = comments)    
    else:
        form_comment_keys = request.form.getlist("deletes")
        for form_comment_key in form_comment_keys:
            db.delete_comments(db.get_comment_id(form_comment_key)[0][0], 1)
        flash("You deleted some of your comments")
        return redirect(url_for("comments_page"))
     
@app.route("/earthquakes", methods=["GET","POST"])
def earthquakes_page():
    db = current_app.config["db"]
    if request.method == "GET":
        earths = db.get_earthquakes(0, 0)
        i = 0
        for earth in earths:
            earths[i] = list(earths[i])
            i = i + 1
        return render_template("earthquakes.html", earths = earths)
    else:
        form_earth_keys = request.form.getlist("deletes")
        for form_earth_key in form_earth_keys:
            db.delete_earthquake(form_earth_key)
        flash("You deleted some of the earthquakes")
        return redirect(url_for("earthquakes_page"))

@app.route("/new_earthquake", methods=["GET","POST"])   
def add_earthquake_page():
    if request.method == "GET":
        return render_template("add_earthquake.html")
    else:
        form_agency = request.form["agency"]
        form_date_time = request.form["date_time"]
        form_latitude = request.form["latitude"]
        form_longitude = request.form["longitude"]
        form_depth = request.form["depth"]
        form_RMS = request.form["RMS"]
        form_kind = request.form["kind"]
        form_magnitude = request.form["magnitude"]
        form_country = request.form["country"]
        form_city = request.form["city"]
        form_village = request.form["village"]
        form_other1 = request.form["other1"]
        form_other2 = request.form["other2"]
        form_other3 = request.form["other3"]
        if form_country == None:
            form_country = '-'
        if form_city == None:
            form_city = '-'
        if form_village == None:
            form_village = '-'
        if form_other1 == None:
            form_other1 = '-'
        if form_other2 == None:
            form_other2 = '-'
        if form_other3 == None:
            form_other3 = '-'
        
        db = current_app.config["db"]
        db.create_earthquake(form_agency, form_date_time, form_latitude, form_longitude, form_depth, form_kind, form_magnitude, form_RMS, form_country, form_city, form_village, form_other1, form_other2, form_other3)
        flash("Earthquake has been added successfully :)")
        return redirect(url_for("add_earthquake_page"))

@app.route("/signout")
def signout_page():
    
    db = current_app.config["db"]
    name = session.get('user_id', 'not set')
    user_id = db.get_user_id(name)
    db.delete_person(user_id[0][0])
    logout_user()
    flash("You are no longer a user of this site :(")
    return redirect(url_for("home_page"))

@app.route("/makeessay", methods=["GET","POST"]) 
def make_essay_page():   
    if request.method =="GET":
        return render_template("makeessay.html")
    else:
        topic = request.form["topic"]
        essay = request.form["essay"]
        print(essay)
        print(topic)
        name = session.get('user_id', 'not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        print(user_id[0])
        db.create_essay(topic, essay, user_id[0][0])
        #next_page = request.args.get("next", url_for("comments_page"))
        #render_template("makecomment.html")
        flash("essay is succesfully published :)")
        return redirect(url_for("make_essay_page"))

@app.route("/essays", methods=["GET","POST"])
def essays_page():
    db = current_app.config["db"]
    if request.method == "GET":
        essays = db.get_essay()
        i = 0
        for essay in essays:
            essays[i] = list(essays[i])
            essays[i][0] = db.get_person(essay[0])[0][0]
            i = i + 1
        return render_template("essay.html", essays = essays)
    else:
        form_essay_keys = request.form.getlist("deletes")
        for form_essay_key in form_essay_keys:
            db.delete_essays(db.get_essay_id(form_essay_key)[0][0],1)
        flash("You deletede some of you essays")
        return redirect(url_for("essays_page"))

@app.route("/makeannouncement", methods=["GET","POST"])
def make_announcement_page():
    if request.method == "GET":
        return render_template("makeannouncement.html")
    else:
        header = request.form["header"]
        announcement = request.form["announcement"]
        print(header)
        print(announcement)
        name = session.get('user_id', 'not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        print(user_id[0])
        db.create_announcement(header, announcement, user_id[0][0])
        flash("announcement is succesfully announced :)")
        return redirect(url_for("make_announcement_page"))

@app.route("/announcements", methods=["GET","POST"])
def announcements_page():
    db = current_app.config["db"]
    if request.method == "GET":
        announcements = db.get_announcement()
        i = 0
        for announcement in announcements:
            announcements[i] = list(announcements[i])
            announcements[i][0] = db.get_person(announcement[0])[0][0]
            i = i + 1
        return render_template("announcement.html", announcements = announcements)
    else:
        form_announcement_keys = request.form.getlist("deletes")
        for form_announcement_key in form_announcement_keys:
            db.delete_announcements(db.get_announcement_id(form_announcement_key)[0][0],1)
        flash("You deletede some of your announcements")
        return redirect(url_for("announcements_page"))

#app.add_url_rule("/", view_func=views.home_page)
#app.add_url_rule("/signup", view_func=views.signup_page, methods=["GET", "POST"])
#app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
#app.add_url_rule("/logout", view_func=views.logout_page)
#app.add_url_rule("/makecomment", view_func=views.make_comment_page,methods=["GET", "POST"])
#app.add_url_rule("/comments", view_func=views.comments_page, methods=["GET","POST"])
#app.add_url_rule("/earthquakes", view_func=views.earthquakes_page, methods = ["GET","POST"])
#app.add_url_rule("/new_earthquake", view_func=views.add_earthquake_page, methods=["GET", "POST"])
#app.add_url_rule("/signout", view_func=views.signout_page)
#app.add_url_rule("/makeessay", view_func=views.make_essay_page,methods=["GET", "POST"])
#app.add_url_rule("/essays", view_func=views.essays_page, methods=["GET","POST"])
#app.add_url_rule("/makeannouncement", view_func=views.make_announcement_page,methods=["GET", "POST"])
#app.add_url_rule("/announcements", view_func=views.announcements_page, methods=["GET","POST"])



app.config["DEBUG"] = True
lm.init_app(app)
lm.login_view = "login_page"

db = d()
app.config["db"] = db

#Session(app)


    

    
if __name__ == "__main__":
   # app = create_app()
    app.run()
