from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])

    password = PasswordField("Password", [validators.DataRequired()])