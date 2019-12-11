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
