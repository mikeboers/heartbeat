from datetime import datetime
import calendar
import time
import logging

from croniter import croniter
import requests

from .main import db

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
        if self.url_to_monitor:
            self._check_url()

    def _check_url(self):

        try:
            req = requests.get(self.url_to_monitor)
            status_code = req.status_code
        except requests.exceptions.Timeout:
            status_code = 604 # This is a custom code for a timeout.
        
        log.debug('"%s" returned %d' % (self.url_to_monitor, status_code))

        beat = Heartbeat(
            service=self,
            time=datetime.utcnow(),
            http_code=status_code,
            remote_addr='127.0.0.1',
            remote_name='localhost',
        )
        self.heartbeats.append(beat)

    @property
    def last_beat(self):
        if not self.heartbeats:
            return
        return max(self.heartbeats, key=lambda h: h.time)

    @property
    def last_time(self):
        beat = self.last_beat
        return beat and beat.time

    def cron_iter(self, start=None):
        if isinstance(start, datetime):
            start = calendar.timegm(start.timetuple())
        return self.cron_spec and croniter(self.cron_spec, start or time.time())

    @property
    def next_expected_time(self):
        iter_ = self.cron_iter()
        return iter_ and datetime.utcfromtimestamp(iter_.get_next())


# Hooray for circular imports!
from .heartbeat import Heartbeat

