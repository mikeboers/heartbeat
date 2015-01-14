import datetime
import logging

from .main import db
from .service import Service


log = logging.getLogger(__name__)


class Heartbeat(db.Model):

    __table__ = db.Table('heartbeats', db.metadata,
        db.Column('time', db.DateTime, default=datetime.datetime.utcnow),
        db.Column('remote_addr', db.String, default='0.0.0.0'),
        db.Column('remote_name', db.String, default='internal'),
        autoload=True,
        autoload_with=db.engine,
    )

    service = db.relationship(Service, backref=db.backref('_heartbeats',
        cascade="all, delete, delete-orphan",
        order_by='Heartbeat.time',
    ))

    def labels(self, as_of=None):

        labels = []

        if self.http_code:
            labels.append((
                'http %d' % self.http_code,
                'success' if self.http_code == 200 else 'important',
            ))

        if self.return_code is not None:
            labels.append((
                'code %d' % self.return_code,
                'success' if not self.return_code else 'important',
            ))

        if self.service.cron_spec:

            next_ = (Heartbeat.query
                .filter(Heartbeat.service == self.service)
                .filter(Heartbeat.time > self.time)
                .order_by(Heartbeat.time)
            ).first()

            # Check to see if the next heartbeat arrived on time (i.e. within
            # the last two cron windows).
            cron = self.service.cron_iter(next_.time if next_ else as_of)
            cron.get_prev()
            window = datetime.datetime.utcfromtimestamp(cron.get_prev())
            if self.time < window:
                labels.append(('stale', 'warning'))

        if not labels:
            labels.append(('ok', 'success'))

        return labels





