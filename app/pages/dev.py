import os

from flask import request

from ..main import app


if not app.config['IS_HEROKU']:
    @app.route('/dev/environ')
    def show_environ():
        return ''.join(_environ_iter()), 200, [('Content-Type', 'text/plain')]

def _environ_iter():
    
    yield 'OS Environ:\n'
    for k, v in sorted(os.environ.iteritems()):
        yield '\t%s: %r\n' % (k, v)

    yield '\n\nWSGI Environ:\n'
    for k, v in sorted(request.environ.iteritems()):
        yield '\t%s: %r\n' % (k, v)
