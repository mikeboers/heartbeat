import logging
from datetime import datetime, timedelta

from .main import app


log = logging.getLogger(__name__)


_plural_s = lambda n: 's' if n != 1 else ''


@app.add_template_filter
def timedeltaformat(delta):

    if isinstance(delta, datetime):
        delta = delta - datetime.utcnow()
    if isinstance(delta, timedelta):
        delta = delta.days * 60 * 60 * 24 + delta.seconds

    future = delta >= 0
    delta = int(abs(delta))
    minutes, seconds = divmod(delta, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    for value, unit in [
        (days, 'day'),
        (hours, 'hour'),
        (minutes, 'minute'),
        (seconds, 'second'),
    ]:
        if value:
            return '%d %s%s %s' % (
                value, unit, _plural_s(value), '' if future else 'ago',
            )
    return 'now'


app.add_template_filter(datetime.utcfromtimestamp)
app.add_template_filter(datetime.fromtimestamp)
