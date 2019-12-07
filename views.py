import pyodbc
from datetime import datetime

from flask import render_template



def earthquakes_page():
    return "bbb"

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def comments_page():
    return "aaaaa"
