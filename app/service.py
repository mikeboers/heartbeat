from .main import db


class Service(db.Model):
    __table__ = db.Table('services', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )


class Component(db.Model):
    __table__ = db.Table('service_components', db.metadata,
        autoload=True,
        autoload_with=db.engine,
    )

    service = db.relationship(Service, backref="components")




