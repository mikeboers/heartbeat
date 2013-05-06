import datetime
import socket

from flask import request

from ..main import app, db
from ..beat import Beat


@app.route('/api/beat', methods=('POST', ))
def handle_beat():

    if app.config['IS_HEROKU']:
        remote_addr = request.access_route[-1]
    else:
        remote_addr = request.remote_addr

    beat = Beat(
        name=request.form.get('name', ''),
        time=datetime.datetime.utcnow(),
        remote_addr=remote_addr,
        remote_name=socket.gethostbyaddr(remote_addr)[0],
    )
    db.session.add(beat)
    db.session.commit()

    return 'ok\n'
