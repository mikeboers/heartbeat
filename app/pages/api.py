import datetime
import logging
import socket

from flask import request, abort, redirect, url_for

from ..main import app, db
from ..service import Service
from ..heartbeat import Heartbeat


log = logging.getLogger(__name__)


@app.route('/api/beat', endpoint='heartbeat_api', methods=('POST', ))
def do_create_heartbeat():

    if app.config['IS_HEROKU']:
        remote_addr = request.access_route[-1]
    else:
        remote_addr = request.remote_addr

    name = request.form.get('name')
    if not name:
        abort(400)

    service = db.session.query(Service).filter(Service.name == name).first()
    if not service:
        log.info('creating service %r' % name)
        service = Service(name=name)
        db.session.add(service)


    beat = Heartbeat(
        service=service,
        time=datetime.datetime.utcnow(),
        remote_addr=remote_addr,
        remote_name=socket.gethostbyaddr(remote_addr)[0],
    )
    db.session.add(beat)
    db.session.commit()

    return 'ok\n'


@app.route('/api/create_service', endpoint='create_service_api', methods=('POST', ))
def do_create_service():

    name = request.form.get('name')
    if not name:
        abort(400)

    service = db.session.query(Service).filter(Service.name == name).first()
    if not service:
        service = Service(name=name)
        db.session.add(service)
        db.session.commit()

    return redirect(url_for('service_details', name=name))


