from flask import render_template

from ..main import app, db
from ..service import Service, Component
from ..heartbeat import Heartbeat


@app.route('/')
def do_index():

    services = db.session.query(Service).all()
    services = [s for s in services if s.components]
    for service in services:
        service.components.sort(key=lambda c: c.heartbeats[0].time, reverse=True)
    services.sort(key=lambda s: s.components[0].heartbeats[0].time, reverse=True)

    return render_template('/services.html', services=services)


@app.route('/services/<name>')
def get_service(name):

    service = db.session.query(Service).filter(Service.name == name).first()
    if not service:
        abort(404)

    service.components.sort(key=lambda c: c.heartbeats[0].time, reverse=True)
    return render_template('/components.html', service=service)

@app.route('/services/<service>/<component>')
def get_component(service, component):

    service = db.session.query(Service).filter(Service.name == service).first()
    if not service:
        abort(404)
    component = db.session.query(Component).filter(Component.service == service).filter(Component.name == component).first()
    if not component:
        abort(404)

    return render_template('/heartbeats.html', component=component)

