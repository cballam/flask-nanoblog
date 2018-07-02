from website import app, db
from flask import Flask, request, session, jsonify
from dbModels import Points, Comments, Blogpost

# send a JSON object with score, post_id, comment_id. Will change to two api routes soon
@app.route('/api/comments', methods=['POST'])
def commentpoints():
    user = session['username']
    obj = request.form
    score = None

    # Find score, if it exists
    score = Points.query.filter_by(user = user).filter_by(comment_id = obj['comment_id']).first()

    # Handle update or create logic
    if score:
        score.updateScore(obj['score'])
    elif obj['comment_id']:
        newScore = Points(score = obj['score'], comment_id = obj['comment_id'], user = session['username'])
        db.session.add(newScore)
    db.session.commit()

    # Return json object with updated point values
    if obj['comment_id']:
        item = Comments.query.filter_by(id = obj['comment_id']).first()
        return jsonify(score = item.getPoints())

    return jsonify(score = 0)

# Second api route for post score
@app.route('/api/posts', methods=['POST'])
def postpoints():
    user = session['username']
    obj = request.form
    score = None

    # Find score, if it exists
    score = Points.query.filter_by(user = user).filter_by(post_id = obj['post_id']).first()

    # Handle update or create logic
    if score:
        score.updateScore(obj['score'])
    elif obj['post_id']:
        newScore = Points(score = obj['score'], post_id = obj['post_id'], user = session['username'])
        db.session.add(newScore)
    db.session.commit()

    # Return json object with updated point values
    if obj['post_id']:
        item = Blogpost.query.filter_by(id = obj['post_id']).first()
        return jsonify(score = item.getPoints())

    return jsonify(score = 0)
