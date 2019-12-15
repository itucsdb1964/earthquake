''' from datetime import datetime

from flask import Flask, render_template
from connection import all_database


app = Flask(__name__)

@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", aaa ="bbb" ,day=day_name)

@app.route("/movies")
def movies_page():
    return "aaaa"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)   '''


from flask import Flask, session

import views
from flask_session import Session

from flask_login import LoginManager
from user import get_user

from tables import database

lm = LoginManager()


app = Flask(__name__)

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)
    
def create_app():
    
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/signup", view_func=views.signup_page, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/makecomment", view_func=views.make_comment_page,methods=["GET", "POST"])
    app.add_url_rule("/comments", view_func=views.comments_page)
    app.add_url_rule("/earthquakes", view_func=views.earthquakes_page)
    app.add_url_rule("/new_earthquake", view_func=views.add_earthquake_page, methods=["GET", "POST"])
    app.add_url_rule("/new_comment", view_func=views.add_comment_page, methods=["GET", "POST"])
    #app.config["DEBUG"] = True
    lm.init_app(app)
    lm.login_view = "login_page"

    db = database()
    app.config["db"] = db

    Session(app)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=TRUE,port=8080)
