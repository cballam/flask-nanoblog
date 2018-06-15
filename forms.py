# Form classes for login, registration

from flask import flash
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo
from dbModels import Users

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')

    # Extend the base validation method to ensure unique usernames
    def validate(self):
        if not Form.validate(self):
            return False

        if (Users.query.filter_by(username = self.username.data).first() is not None):
            flash("This username is already taken - try another one", "warning")
            return False

        return True

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=4, max=140)])
    topic = StringField('Topic')
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=10, max=10000)])

class UpdatePostForm(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=10, max=10000)])

class CommentForm(FlaskForm):
    content = TextAreaField('', validators=[InputRequired(), Length(min=10, max=10000)])

class SearchForm(FlaskForm):
    search = StringField('', validators=[InputRequired()])
