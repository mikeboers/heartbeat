from datetime import datetime

from croniter import croniter

from .main import db


class Service(db.Model):
    __table__ = db.Table('services', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    @property
    def last_beat(self):
        if not self.heartbeats:
            return
        return max(self.heartbeats, key=lambda h: h.time)

    @property
    def last_time(self):
        beat = self.last_beat
        return beat and beat.time

    @property
    def cron_iter(self):
        return self.cron_spec and croniter(self.cron_spec)

    @property
    def next_expected_time(self):
        iter_ = self.cron_iter
        return iter_ and datetime.utcfromtimestamp(iter_.get_next())



