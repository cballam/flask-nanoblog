# Form classes for login, registration

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=4, max=140)])
    subtitle = StringField('Subtitle')
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=10, max=10000)])

class UpdatePostForm(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=10, max=10000)])

class ReplyForm(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=10, max=10000)])
