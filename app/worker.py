import time
import sys
import logging
import math
import datetime

import requests
from croniter import croniter

from .main import db
from .service import Service
from .heartbeat import Heartbeat
from . import config


log = logging.getLogger(__name__)


def main():

    next_time = int(time.time() + 60) / 60 * 60
    while True:
        now = time.time()
        to_wait = math.ceil(next_time - now)
        if to_wait > 0:
            print >> sys.stderr, 'worker sleeping for %ds' % to_wait
            time.sleep(to_wait)
            continue

        for service in db.session.query(Service):

            if service.url_to_monitor and service.cron_spec:
                cron = croniter(service.cron_spec, next_time - 1)
                cron_next = cron.get_next()
                if cron_next == next_time:

                    try:
                        req = requests.get(service.url_to_monitor)
                        status_code = req.status_code
                    except requests.exceptions.Timeout:
                        status_code = 604 # This is a custom code for a timeout.
                    
                    log.debug('check of "%s" returned %d for "%s"' % (service.name, status_code, service.url_to_monitor))

                    beat = Heartbeat(
                        service=service,
                        time=datetime.datetime.utcnow(),
                        http_code=status_code,
                        remote_addr='127.0.0.1',
                        remote_name='localhost',
                    )
                    service.heartbeats.append(beat)

                else:
                    log.debug('next check of "%s" in %ds' % (service.name, math.ceil(cron_next - now)))

            # Clean up excess heartbeats.
            if len(service.heartbeats) > config.HEARTBEATS_PER_SERVICE:
                service.heartbeats.sort(key=lambda h: h.time, reverse=True)
                service.heartbeats[config.HEARTBEATS_PER_SERVICE:] = []

        db.session.commit()
        next_time += 60







if __name__ == '__main__':
    main()
