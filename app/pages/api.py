import datetime
import logging
import socket

from flask import request, abort, redirect, url_for

from ..main import app, db
from ..service import Service, Component
from ..heartbeat import Heartbeat


log = logging.getLogger(__name__)


@app.route('/api/beat', methods=('POST', ))
def handle_beat():

    if app.config['IS_HEROKU']:
        remote_addr = request.access_route[-1]
    else:
        remote_addr = request.remote_addr

    service_name = request.form.get('service')
    name = request.form.get('name')
    if not service_name and name:
        service_name = name
        name = 'main'
    if not service_name or not name:
        abort(400)

    service = db.session.query(Service).filter(Service.name == service_name).first()
    if not service:
        log.info('creating service %r' % service_name)
        service = Service(name=service_name)
        db.session.add(service)

    component = db.session.query(Component).filter(Component.service == service).filter(Component.name == name).first()
    if not component:
        log.info('creating component %r / %r' % (service_name, name))
        component = Component(service=service, name=name)
        db.session.add(component)

    beat = Heartbeat(
        component=component,
        time=datetime.datetime.utcnow(),
        remote_addr=remote_addr,
        remote_name=socket.gethostbyaddr(remote_addr)[0],
    )
    db.session.add(beat)
    db.session.commit()

    return 'ok\n'


@app.route('/api/create_service', methods=('POST', ))
def post_create_service():

    name = request.form.get('name')
    if not name:
        abort(400)

    service = db.session.query(Service).filter(Service.name == name).first()
    if not service:
        service = Service(name=name)
        db.session.add(service)
        db.session.commit()

    return redirect(url_for('get_service', name=name))


@app.route('/api/create_component', methods=('POST', ))
def post_create_component():


    name = request.form.get('name')
    if not name:
        abort(400)

    try:
        service_id = int(request.form.get('service_id'))
    except ValueError:
        abort(400)

    service = db.session.query(Service).get(service_id)
    if not service:
        abort(404)


    component = db.session.query(Component).filter(Component.service == service).filter(Component.name == name).first()
    if not component:
        component = Component(service=service, name=name)
        db.session.add(component)
        db.session.commit()

    return redirect(url_for('get_component', service=service.name, component=name))
