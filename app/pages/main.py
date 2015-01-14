import datetime

from flask.ext.mako import render_template

from ..main import app, db
from ..service import Service
from ..heartbeat import Heartbeat


epoch = datetime.datetime(1970, 1, 1)


@app.route('/', endpoint='index')
def do_index():
    services = db.session.query(Service).all()
    services.sort(key=lambda s: s.last_time or epoch, reverse=True)
    return render_template('/index.html', services=services)


@app.route('/services/<name>', endpoint='service_details')
def do_service_details(name):
    service = db.session.query(Service).filter(Service.name == name).first()
    if not service:
        abort(404)
    heartbeats = (Heartbeat.query
        .filter(Heartbeat.service == service)
        .order_by(Heartbeat.time.desc())
    )[:10]
    return render_template('/service.html',
        service=service,
        heartbeats=heartbeats,
    )
