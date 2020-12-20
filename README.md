# Archived

This has not been worked on for 18 months, and I have no plans to update the project.

# flask-nanoblog

flask-nanoblog is a relatively simplistic blogging/social media platform which provides CRUD functionality. It has taken inspiration from various tutorials and websites, most notably "flask_reddit" [linked here](https://github.com/codelucas/flask_reddit) as well as reddit itself (and related social media websites)

This repo utilizes:

- Flask as the backend framework
- nginx and gunicorn as the preferred HTTP/wsgi server for a practical implementation
- sqlite3 as the database (standard with any python installation)
- flask-sqlalchemy to interact with said database
- Flask_Bootstrap and WTForms to make the front-end look acceptable
- Flask-Cache as a caching service to ensure good performance

## Current Features:

- User registration/login (with relatively secure password hashing)
- Individual profile pages
- Posting, updating and deleting of posts
- Post title searching
- Threaded comments on posts
- Topic pages similar to Reddit's subreddit system

## In progress:

- More useful search feature (ongoing)
- Voting on posts (working on UI)

## Planned:

- Email validation of users and features such as password resets (utilising Celery/Rabbitmq)
- Make the UI look better (maybe)
- Subreddit-like "topic" section, with popular "topics" shown in sidebar
