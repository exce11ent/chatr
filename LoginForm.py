__author__ = 'Vitalii Krayovyi'

from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class MessageForm(Form):
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])