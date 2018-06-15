# Sets all of the routes for the app
from website import app, cache
from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import LoginForm, RegisterForm, AddPostForm, UpdatePostForm, SearchForm, CommentForm
from dbModels import Blogpost, Users, Comments
from datetime import datetime
from website import db, cache
from functools import wraps
from werkzeug import generate_password_hash, check_password_hash

# Decorator to require user be logged in
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if (session.get('username')):
            return f(*args, **kwargs)
        else:
            flash('You need to be logged in to access this', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=15)
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search', query=form.search.data))
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts, form=form)

@app.route('/about')
def about():
    return render_template('about.html')

# View individual post
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()

    # Submit the comment if the form validates
    if form.validate_on_submit():
        comment = Comments(post = post_id, author = session.get('username'), \
            date_posted = datetime.now(), content = form.content.data)
        db.session.add(comment)
        db.session.commit()
        form.content.data = ""

    post = Blogpost.query.filter_by(id=post_id).one()
    comments = post.getComments()
    return render_template('post.html', post=post, comments=comments, form=form)

# Update individual post if author is logged in
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    updateForm = UpdatePostForm()
    post = Blogpost.query.filter_by(id=post_id).one()
    if (session.get('username') != post.author):
        flash('You are not authorized to do this', 'danger')
        return redirect(url_for('post', post_id = post_id))

    if updateForm.validate_on_submit():
        post.content = updateForm.content.data
        db.session.commit()
        return redirect(url_for('post', post_id = post_id))
    updateForm.content.data = post.content;
    return render_template('update.html', form=updateForm, post=post)

# Delete post if the author is logged in
@app.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    if post.author == session['username']:
        db.session.delete(post)
        db.session.commit()
        flash('Deleted post', 'danger')
        return redirect(url_for('profile', username = session['username']))
    flash('Cannot delete post', 'danger')
    return redirect(url_for('post', post_id=post_id))

# Delete comment if author is logged in
@app.route('/deleteComment/<int:post_id>/<int:comment_id>')
@login_required
def deleteComment(post_id, comment_id):
    comment = Comments.query.filter_by(id=comment_id).one()
    if comment.author == session['username']:
        db.session.delete(comment)
        db.session.commit()
        flash('Deleted comment', 'danger')
        return redirect(url_for('post', post_id=post_id))
    flash('Cannot delete post', 'danger')
    return redirect(url_for('index'))

# Adds a post
@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
    form = AddPostForm()
    if form.validate_on_submit():
        title = form.title.data
        topic = form.topic.data
        author = session['username']
        content = form.content.data

        post = Blogpost(title=title, topic=topic, author=author, \
        content=content, date_posted=datetime.now())

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('profile', username = session['username']))
    return render_template('add.html', form=form)

# Logs a user in, sets a session variable
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                session['username'] = form.username.data
                flash('Logged in as ' + session['username'], 'success')
                return redirect(url_for('index'))
            flash('Incorrect password', 'danger')
            return render_template('login.html', form=form)
        flash('User does not exist', 'danger')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

# Logs a user out, pops session var
@app.route('/logout')
@login_required
def logout():
    form = LoginForm()
    session.pop('username', None)
    flash('Successfully logged out', 'success')
    return render_template('login.html', form=form)

# Registers a new user and directs them to the login form
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data, 'sha256')
        newUser = Users(username = username, password = password)

        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Displays the profile of the desired user
@app.route('/profile/<username>')
def profile(username):
    posts = Blogpost.query.filter_by(author=username).order_by(Blogpost.date_posted.desc()).all()
    return render_template('profile.html', posts=posts, username = username)

# Searches the database for relevant content
@app.route('/search/<query>', methods=['GET', 'POST'])
def search(query):
    form = SearchForm()
    form.search.data = query

    results = Blogpost.query.filter(Blogpost.title.like("%" + str(query) + "%")).\
    order_by(Blogpost.date_posted.desc()).all()

    return render_template('search.html', results=results, form=form)

# Shows posts with the defined topic
@app.route('/t/<topic>')
def topic(topic):
    form = SearchForm()
    posts = Blogpost.query.filter_by(topic=topic).order_by(Blogpost.date_posted.desc()).all()
    return render_template('topic.html', posts=posts, topic=topic, form=form)
