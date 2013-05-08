from .main import db
from .service import Service


class Heartbeat(db.Model):
    __table__ = db.Table('heartbeats', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    service = db.relationship(Service, backref='heartbeats')




