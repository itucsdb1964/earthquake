from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def get_user(user_id):
    password = current_app.config["db"].get_password(user_id)
    user = User(user_id, password) if password else None
    if user is not None:
        user.is_admin = current_app.config["db"].get_type(user_id)
    return user