# User and Post models
from website import db

# Note that sqlite3 doesn't have string types, and stores these as "TEXT".
# Data is formatted this way so that the blog is compatible with other databases

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

class Users(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(80))

class Replies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply_to_post = db.Column(db.Integer)
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
