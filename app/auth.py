from flask import request, redirect, session, url_for, Response
from flask.ext.mako import render_template

from .main import app


USERNAME = app.config['USERNAME']
PASSWORD = app.config['PASSWORD']


@app.before_request
def assert_authenticated():

    if USERNAME is None or PASSWORD is None:
        return

    user = session.get('user')
    if user is None and request.endpoint not in ('login', 'logout'):
        return redirect(url_for('login'))


@app.route('/login', endpoint='login', methods=['GET', 'POST'])
def handle_login():

    username = request.form.get('username')
    password = request.form.get('password')

    if username == USERNAME and password == PASSWORD:
        session['user'] = username
        return redirect(url_for('index'))

    else:
        return render_template('/login.html')


@app.route('/logout', endpoint='logout')
def handle_logout():
    session.pop('user')
    return redirect(url_for('index'))
