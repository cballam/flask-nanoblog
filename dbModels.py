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

    def getComments(self):
        return Comments.query.filter_by(post = self.id).filter_by(parent=-1).order_by(Comments.date_posted.desc()).all()

    def getPoints(self):
        points = db.session.query(Points.score).\
        filter_by(post_id = self.id).all()
        if not points:
            return 0
        points = sum(item[0] for item in points)
        return points

    # Used to find the button color (check if user has voted up)
    def upColor(self, user):
        score = Points.query.filter_by(post_id = self.id).filter_by(user = user).first()
        if (not score) or (score.score == 0 or score.score == -1):
            return "lightgray"
        else:
            return "green"
        # default
        return "lightgray"

    def downColor(self, user):
        score = Points.query.filter_by(post_id = self.id).filter_by(user = user).first()
        if (not score) or score.score == 0 or score.score == 1:
            return "lightgray"
        else:
            return "red"
        return "lightgray"


# Typical user has only a username and password.
# Possibly add email verification and support later
class Users(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(80))

# Keep comments as simply replies to a post. No nesting yet
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer)
    parent = db.Column(db.Integer)
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

    def getComments(self):
        return Comments.query.filter_by(parent = self.id)\
        .order_by(Comments.date_posted.desc()).all()

    # returns total score of the comment
    def getPoints(self):
        points = db.session.query(Points.score).\
        filter_by(comment_id = self.id).all()
        if not points:
            return 0
        points = sum(item[0] for item in points)
        return points

    # Used to find the button color (check if user has voted up)
    def upColor(self, user):
        score = Points.query.filter_by(comment_id = self.id).filter_by(user = user).first()
        if not score or score.score == 0 or score.score == -1:
            return "lightgray"
        else:
            return "green"
        # default
        return "lightgray"

    def downColor(self, user):
        score = Points.query.filter_by(comment_id = self.id).filter_by(user = user).first()
        if not score or score.score == 0 or score.score == 1:
            return "lightgray"
        else:
            return "red"
        return "lightgray"

# Topics each have a name and short description
class Topics(db.Model):
    name = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.String(200))

class Points(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(20))
    comment_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    score = db.Column(db.Integer) # -1, 0, 1

    # Updates the score of the object, doesn't allow multiple "upvotes"
    def updateScore(self, score):
        if int(self.score) == int(score):
            self.score = 0
        else:
            self.score = score
        db.session.commit()
