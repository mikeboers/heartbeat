import time
import sys
import logging
import math
import datetime

from croniter import croniter

from .main import app, db
from .service import Service
from .heartbeat import Heartbeat
from . import config


log = logging.getLogger(__name__)


def main():
    with app.app_context():
        with app.test_request_context('/worker'):
            _main()

def _main():

    next_time = int(time.time() + 60) / 60 * 60
    last_time = next_time - 60

    while True:

        # Wait for the full minute to pass.
        now = time.time()
        to_wait = math.ceil(next_time - now)
        if to_wait > 0:
            print >> sys.stderr, 'worker sleeping for %ds' % to_wait
            time.sleep(to_wait)
            continue

        for service in db.session.query(Service):
            with service.notify_context(last_time, next_time):
                if service.cron_spec and service.can_active_check:

                    # See if the next time to run is within the bracket that
                    # just passed.
                    cron = croniter(service.cron_spec, last_time)
                    cron_next = cron.get_next()
                    if cron_next <= next_time:
                        log.debug('checking "%s"...' % service.name)
                        service.active_check()

                    else:
                        log.debug('next check of "%s" in %ds' % (service.name, math.ceil(cron_next - now)))

        db.session.commit()
        last_time = next_time
        next_time += 60



if __name__ == '__main__':
    main()
