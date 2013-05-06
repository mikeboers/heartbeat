from flask import render_template

from ..main import app, db
from ..beat import Beat


@app.route('/')
def index():
    beats = db.session.query(Beat).all()
    return render_template('index.html', beats=beats)

