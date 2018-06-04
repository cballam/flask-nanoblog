from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_cache import Cache

app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from routing import *

if __name__ == '__main__':
    app.run()
