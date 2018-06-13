# User and Post models
from website import db
from datetime import datetime

# Note that sqlite3 doesn't have string types, and stores these as "TEXT".
# Data is formatted this way so that the blog is compatible with other databases

# Each post has unique ID. May need to add or change topic
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

# Typical user has only a username and password.
# Possibly add email verification and support later
class Users(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(80))

# Keep comments as simply replies to a post. No nesting yet
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer)
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

    # Reddit-like date format
    def timeFormat(self):
        currently = datetime.now()
        difference = currently - self.date_posted

        seconds = difference.seconds
        days = difference.days

        if days == 0:
            if seconds < 60:
                return f"{seconds} seconds ago"
            if seconds < 120:
                return "1 minute ago"
            if seconds < 3600:
                return f"{int(seconds/60)} minutes ago"
            if seconds < 7200:
                return "1 hour ago"
            if seconds < 86400:
                return f"{int(seconds/3600)} hours ago"

        else:
            if days == 1:
                return "Yesterday"
            if days < 7:
                return f"{days} days ago"
            if days < 30:
                return f"{int(days/7)} weeks ago"
            if days < 365:
                return f"{int(days/30)} months ago"

        return f"{days/365} years ago"

# Topics each have a name and short description
class Topics(db.Model):
    name = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.String(200))
