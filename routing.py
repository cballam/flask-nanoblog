# Sets all of the routes for the app
from website import app
from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import LoginForm, RegisterForm, AddPostForm, UpdatePostForm, SearchForm
from dbModels import Blogpost, Users
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

@cache.cached(timeout=60)
@app.route('/', methods=['GET', 'POST'])
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
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)

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
        return redirect(url_for('index'))
    flash('Cannot delete post', 'danger')
    return redirect(url_for('post', post_id=post_id))

# Adds a post
@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
    form = AddPostForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        author = session['username']
        content = form.content.data

        post = Blogpost(title=title, subtitle=subtitle, author=author, \
        content=content, date_posted=datetime.now())

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
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
    results = Blogpost.query.filter(Blogpost.title.like("%" + str(query) + "%")).order_by(Blogpost.date_posted.desc()).all()
    return render_template('search.html', results=results, form=form)
