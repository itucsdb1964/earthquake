import pyodbc
from datetime import datetime

from flask import current_app, render_template,request,redirect,url_for

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
    return "bbb"

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def comments_page():
    return "aaaaa"
