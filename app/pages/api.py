import datetime

from flask import request

from ..main import app, db
from ..beat import Beat


@app.route('/api/beat')
def handle_beat():

    beat = Beat(name='testing', time=datetime.datetime.utcnow())
    db.session.add(beat)
    db.session.commit()

    return 'ok'
