import datetime

from .main import db


epoch = datetime.datetime(1970, 1, 1)


class Service(db.Model):
    __table__ = db.Table('services', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    @property
    def latest_time(self):
        if not self.components:
            return epoch
        return max(self.components, key=lambda c: c.latest_time).latest_time


class Component(db.Model):
    __table__ = db.Table('service_components', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    service = db.relationship(Service, backref="components")

    @property
    def latest_time(self):
        if not self.heartbeats:
            return epoch
        return max(self.heartbeats, key=lambda h: h.time).time




