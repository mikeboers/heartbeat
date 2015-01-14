from contextlib import contextmanager
from datetime import datetime
import calendar
import time
import logging

from croniter import croniter
import requests
from flask import request
from flask.ext.mako import render_template
from .main import app, db
from .mail import sendmail

log = logging.getLogger(__name__)


class Service(db.Model):

    __table__ = db.Table('services', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    @property
    def can_active_check(self):
        return bool(self.url_to_monitor)

    def active_check(self):
        try:
            if self.url_to_monitor:
                self._check_url()
        except Exception as e:
            Heartbeat(
                service=self,
                return_code=1,
                description=repr(e).strip(),
            )

    def _check_url(self):

        try:
            res = requests.get(self.url_to_monitor)
            status_code = res.status_code
            description = res.headers['status']
        except requests.exceptions.RequestException as e:
            status_code = 600 # This is a custom code for a timeout.
            description = repr(e).strip()
        
        log.debug('"%s" returned %d: %r' % (self.url_to_monitor, status_code,
            description))

        Heartbeat(
            service=self,
            http_code=status_code,
            description=description,
        )

    @property
    def heartbeat_count(self):
        return Heartbeat.query.filter(Heartbeat.service == self).count()

    @property
    def last_beat(self):
        return (Heartbeat.query
            .filter(Heartbeat.service == self)
            .order_by(Heartbeat.time.desc())
        ).first()

    @property
    def last_time(self):
        beat = self.last_beat
        return beat and beat.time

    def last_labels(self, at=None):
        beat = self.last_beat
        return beat and beat.labels(at)

    def cron_iter(self, start=None):
        if isinstance(start, datetime):
            start = calendar.timegm(start.timetuple())
        return self.cron_spec and croniter(self.cron_spec, start or time.time())

    @property
    def next_expected_time(self):
        iter_ = self.cron_iter()
        return iter_ and datetime.utcfromtimestamp(iter_.get_next())

    @contextmanager
    def notify_context(self, old_time=None, new_time=None):
        old_labels = self.last_labels(old_time)
        yield
        new_labels = self.last_labels(new_time)
        if old_labels != new_labels:
            self.notify(old_labels, new_labels)

    def notify(self, old_labels, new_labels):

        log.info('%s state changed from %r to %r' % (self.name, old_labels, new_labels))

        subject = 'Status change on "%s"' % self.name
        body = render_template('/emails/state_change.txt',
            old_labels=old_labels,
            new_labels=new_labels,
        )
        html = render_template('/emails/state_change.html',
            old_labels=old_labels,
            new_labels=new_labels,
        )

        if app.config['NOTIFY_EMAIL']:
            sendmail(
                recipients=[app.config['NOTIFY_EMAIL']],
                subject=subject,
                body=body,
                html=html,
            )

        if app.config['NOTIFY_PROWL']:
            requests.post('https://api.prowlapp.com/publicapi/add', data=dict(
                apikey=app.config['NOTIFY_PROWL'],
                application='Heartbeat',
                event=self.name,
                description=body,
            ))

        if app.config['NOTIFY_ANDROID']:
            requests.post('https://www.notifymyandroid.com/publicapi/notify', data=dict(
                apikey=app.config['NOTIFY_ANDROID'],
                application='Heartbeat',
                event=self.name,
                description=body,
                priority='0',
            ))


# Hooray for circular imports!
from .heartbeat import Heartbeat

