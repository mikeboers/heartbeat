import datetime
import logging

from .main import db
from .service import Service


log = logging.getLogger(__name__)


class Heartbeat(db.Model):
    __table__ = db.Table('heartbeats', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    service = db.relationship(Service, backref=db.backref('heartbeats', cascade="all, delete, delete-orphan"))

    def labels(self, as_of=None):

        # This is not the most efficient by any means.
        all_next = sorted((h for h in self.service.heartbeats if h.time > self.time), key=lambda h: h.time)
        next_ = all_next[0] if all_next else None
        all_prev = sorted((h for h in self.service.heartbeats if h.time < self.time), key=lambda h: h.time)
        prev = all_prev[-1] if all_prev else None
        # log.debug('siblings: %s < %s < %s' % (prev and prev.time, self.time, next_ and next_.time))

        labels = []

        if self.http_code:
            labels.append(('http %d' % self.http_code, 'success' if self.http_code == 200 else 'important'))
        if self.return_code is not None:
            labels.append(('code %d' % self.return_code, 'success' if not self.return_code else 'important'))

        if self.service.cron_spec:

            # Check to see if the next heartbeat arrived on time.
            cron = self.service.cron_iter(next_.time if next_ else as_of)
            cron.get_prev()
            window = datetime.datetime.utcfromtimestamp(cron.get_prev())
            if self.time < window:
                labels.append(('stale', 'warning'))


        if not labels:
            labels.append(('ok', 'success'))

        # log.debug('labels: %r' % labels)
        return labels





