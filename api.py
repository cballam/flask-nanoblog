from website import app, db
from flask import Flask, request, session, jsonify
from dbModels import Points

# send a JSON object with score, post_id
@app.route('/api/points', methods=['POST'])
def points():
    user = session['username']
    obj = request.form
    score = Points.query.filter_by(user = user).filter_by(post_id = obj['post_id']).first()
    if score:
        score.updateScore(obj['score'])
    else:
        newScore = Points(score = obj['score'], post_id = obj['post_id'], user = session['username'])
        db.session.add(newScore)
    db.session.commit()
    # If nothing is returned, view won't work. Currently keeping the return value static
    # Will change to have it return the jsonified color of the button, so that it can be
    # either green or gray depending on the updated score
    return jsonify(obj)
