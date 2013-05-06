from datetime import datetime, timedelta

from .main import app


_plural_s = lambda n: 's' if n != 1 else ''


@app.add_template_filter
def timedeltaformat(delta):

    if not isinstance(delta, timedelta):
        delta = datetime.utcnow() - delta

    if delta.days:
        return '%d day%s ago' % (delta.days, _plural_s(delta.days))
    if delta.seconds > 3600:
        hours = delta.seconds / 3600
        return '%d hour%s ago' % (hours, _plural_s(hours))
    if delta.seconds > 60:
        minutes = delta.seconds / 60
        return '%d minute%s ago' % (minutes, _plural_s(minutes))

    return '%d second%s ago' % (delta.seconds, _plural_s(delta.seconds))

