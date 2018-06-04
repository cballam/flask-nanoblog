import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/blog.db'
SECRET_KEY = 'secret'
