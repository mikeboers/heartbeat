import logging
import os
import sys


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


from flask import Flask
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.root_path = os.path.abspath(os.path.join(__file__, '..', '..'))
app.config.from_object('app.config')


babel = Babel(app)
db = SQLAlchemy(app)


# Register models.
from . import beat

db.create_all()


# Register routes.
from .pages import api, dev, index

from . import viewutils




