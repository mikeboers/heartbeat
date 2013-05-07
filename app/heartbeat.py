from .main import db
from .service import Component


class Heartbeat(db.Model):
    __table__ = db.Table('heartbeats', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    component = db.relationship(Component,
        backref=db.backref('heartbeats', order_by=__table__.c.time.desc()),
    )




