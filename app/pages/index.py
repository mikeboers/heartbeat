from flask import render_template

from ..main import app, db
from ..service import Service
from ..heartbeat import Heartbeat


@app.route('/')
def index():

    services = db.session.query(Service).all()
    services = [s for s in services if s.components]
    for service in services:
        service.components.sort(key=lambda c: c.heartbeats[0].time, reverse=True)
    services.sort(key=lambda s: s.components[0].heartbeats[0].time, reverse=True)

    heartbeats = db.session.query(Heartbeat).order_by(Heartbeat.time.desc()).all()
    return render_template('index.html', services=services, heartbeats=heartbeats)

