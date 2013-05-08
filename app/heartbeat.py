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

    def labels(self):

        # This is not the most efficient by any means.
        all_next = sorted((h for h in self.service.heartbeats if h.time > self.time), key=lambda h: h.time)
        next_ = all_next[0] if all_next else None
        all_prev = sorted((h for h in self.service.heartbeats if h.time < self.time), key=lambda h: h.time)
        prev = all_prev[-1] if all_prev else None
        log.debug('siblings: %s < %s < %s' % (prev and prev.time, self.time, next_ and next_.time))

        labels = []
        if self.http_code:
            labels.append(('http %d' % self.http_code, 'success' if self.http_code == 200 else 'important'))

        if self.service.cron_spec:

            # This is the latest one; make sure it is within the last two
            # periods.
            if next_ is None:
                cron = self.service.cron_iter()
                cron.get_prev()
                window = datetime.datetime.utcfromtimestamp(cron.get_prev())
                log.debug('window from now is %s' % window)
                if self.time < window:
                    labels.append(('late', 'warning'))

            # It was late if it was two periods from the previous.
            elif prev is not None:
                cron = self.service.cron_iter(prev.time)
                cron.get_next()
                window = datetime.datetime.utcfromtimestamp(cron.get_next())
                log.debug('window from prev is %s' % window)
                if self.time > window:
                    labels.append(('late', 'warning'))


        if not labels:
            labels.append(('ok', 'success'))

        # log.debug('labels: %r' % labels)
        return labels





