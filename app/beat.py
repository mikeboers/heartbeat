from .main import db


class Beat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String, nullable=True)
    time = db.Column(db.DateTime, nullable=False)

