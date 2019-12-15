
from datetime import datetime

from flask import current_app, render_template, request, redirect, url_for, session, flash

from tables import database as d
from flask_session import Session



from datetime import datetime

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


@app.route("/new_earthquake")
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


if __name__ == "__main__":
    app.run( debug=True, port=8080)
