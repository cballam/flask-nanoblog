# flask-nanoblog

flask-nanoblog is a relatively simplistic blogging platform which provides CRUD functionality. It has been made mostly for learning purposes, and was approached with the mindset that a functional site is better than a non-functional site with fantastic code quality (but code quality was kept in mind).

This repo utilizes:

- 'flask' as the backend code
- 'nginx' and 'gunicorn' as the preferred HTTP/wsgi server for a practical implementation
- 'sqlite3' as the database (standard with any python installation)
- 'flask-sqlalchemy' to interact with said database
- 'Flask_Bootstrap' and 'WTForms' to make the front-end look acceptable
- 'Flask-Cache' as a caching service to ensure good performance

## Current Features:

- User registration/login (with relatively secure password hashing)
- Individual profile pages
- Posting, updating and deleting of posts
- Post title searching
- Threaded comments on posts
- Topic pages similar to Reddit's subreddit system

## In progress:

- Front-end changes to the comments to make things less ugly
- More useful search feature

## Planned:

- Voting on posts (through the use of ajax and an api)
- Email validation of users and features such as password resets (utilising Celery/Rabbitmq)
- Make the UI look better (maybe)
