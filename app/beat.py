from .main import db


class Beat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    remote_addr = db.Column(db.String, nullable=False)


