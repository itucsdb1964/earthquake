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


from flask import Flask

import views

    
def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/comments", view_func=views.comments_page)
    app.add_url_rule("/earthquakes", view_func=views.earthquakes_page)
    app.config["DEBUG"] = True
    

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
