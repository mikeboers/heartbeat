import logging
import os
import sys


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


from flask import Flask
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')
app.root_path = app.config['ROOT_PATH']


babel = Babel(app)
db = SQLAlchemy(app)


# Register models.
from . import service
from . import heartbeat
from . import agent


# Register routes.
from .pages import api, dev, index

from . import viewutils




