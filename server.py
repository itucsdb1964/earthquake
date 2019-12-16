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
    app.add_url_rule("/comments", view_func=views.comments_page, methods=["GET","POST"])
    app.add_url_rule("/earthquakes", view_func=views.earthquakes_page)
    app.add_url_rule("/new_earthquake", view_func=views.add_earthquake_page, methods=["GET", "POST"])
    app.add_url_rule("/signout", view_func=views.signout_page)
    app.add_url_rule("/makeessay", view_func=views.make_essay_page,methods=["GET", "POST"])
    app.add_url_rule("/essays", view_func=views.essays_page, methods=["GET","POST"])
    app.add_url_rule("/makeannouncement", view_func=views.make_announcement_page,methods=["GET", "POST"])
    app.add_url_rule("/announcements", view_func=views.announcements_page, methods=["GET","POST"])
    
    

    app.config["DEBUG"] = True
    lm.init_app(app)
    lm.login_view = "login_page"

    db = database()
    app.config["db"] = db

    Session(app)


    return app

    
if __name__ == "__main__":
    app = create_app()
    app.run()
