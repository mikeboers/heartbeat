import logging
import os
import sys


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


from flask import Flask
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mako import MakoTemplates as MakoTemplates


class App(Flask):

    def update_template_context(self, context):
        context.update(self.jinja_env.filters)
        return super(App, self).update_template_context(context)


app = App(__name__)
app.config.from_object('app.config')
app.root_path = app.config['ROOT_PATH']

babel = Babel(app)
db = SQLAlchemy(app)
mako = MakoTemplates(app)

from . import auth

# Register models.
from . import service
from . import heartbeat


# Register routes.
from .pages import api, dev, main

# Register view utilities.
from . import viewutils




