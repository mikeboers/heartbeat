import datetime

from flask import request

from ..main import app, db
from ..beat import Beat


@app.route('/api/beat', methods=('POST', ))
def handle_beat():

    beat = Beat(
        name=request.form.get('name', ''),
        time=datetime.datetime.utcnow(),
        remote_addr=request.remote_addr,
    )
    db.session.add(beat)
    db.session.commit()

    return 'ok'
