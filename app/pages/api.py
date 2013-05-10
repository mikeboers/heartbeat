import datetime
import logging
import socket
import re

from croniter import croniter
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
        return 'missing name', 400

    service = db.session.query(Service).filter(Service.name == name).first()
    if not service:
        log.info('creating service %r' % name)
        service = Service(name=name)
        db.session.add(service)

    return_code = request.form.get('return_code')
    if return_code:
        try:
            return_code = int(return_code)
        except ValueError:
            return 'bad return_code', 400


    beat = Heartbeat(
        service=service,
        time=datetime.datetime.utcnow(),
        remote_addr=remote_addr,
        remote_name=socket.gethostbyaddr(remote_addr)[0],
        return_code=return_code,
        description=request.form.get('description'),
    )
    db.session.add(beat)
    db.session.commit()

    return 'ok\n'


@app.route('/api/beat/delete', endpoint='delete_heartbeat_api', methods=('POST', ))
def do_delete_heartbeat():

    try:
        id_ = int(request.form['id'])
    except KeyError:
        return 'missing id', 400
    except ValueError:
        return 'malformed id', 400

    heartbeat = db.session.query(Heartbeat).get(id_)
    if not heartbeat:
        return 'no heartbeat %d' % (id_, ), 404

    db.session.delete(heartbeat)
    db.session.commit()
    return 'deleted heartbeat %d' % (id_, ), 200


@app.route('/api/service/create', endpoint='create_service_api', methods=('POST', ))
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


@app.route('/api/service/edit', endpoint='edit_service_api', methods=('POST', ))
def do_edit_service():

    try:
        id_ = int(request.form['pk'])
        field = request.form['name']
        value = request.form['value']
    except ValueError:
        return 'malformed pk', 400
    except KeyError as e:
        return 'missing %s' % e.args[0], 400

    service = db.session.query(Service).get(id_)
    if not service:
        return 'invalid pk', 400

    if field == 'url_to_monitor':
        if value and not re.match(r'^https?://[^/]+\.\w+($|/)', value):
            return 'invalid value: must be like http(s)://example.com', 400
        service.url_to_monitor = value or None

    elif field == 'cron_spec':
        if value:
            value = value.strip()
        if value:
            try:
                croniter(value)
            except ValueError:
                return 'invalid CRON spec', 400
        service.cron_spec = value or None

    else:
        return 'invalid field', 400

    db.session.commit()

    return 'updated service[%d].%s' % (id_, field)


@app.route('/api/service/check', endpoint='check_service_api', methods=('POST', ))
def do_check_service():

    try:
        id_ = int(request.form['id'])
    except KeyError:
        return 'missing id', 400
    except ValueError:
        return 'malformed id', 400

    service = db.session.query(Service).get(id_)
    if not service:
        return 'invalid id', 400

    if not service.can_active_check:
        return 'service does not have active check', 412

    service.active_check()
    db.session.commit()
    return 'ok\n'


@app.route('/api/service/delete', endpoint='delete_service_api', methods=('POST', ))
def do_delete_service():

    try:
        id_ = int(request.form['id'])
    except KeyError:
        return 'missing id', 400
    except ValueError:
        return 'malformed id', 400

    service = db.session.query(Service).get(id_)
    if not service:
        return 'no service %d' % (id_, ), 404

    db.session.delete(service)
    db.session.commit()
    return 'deleted service %d' % (id_, ), 200


