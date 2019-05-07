from __future__ import absolute_import, division, print_function

from logging import *
from logging.handlers import HTTPHandler

import requests
from middleware.thread_local import get_current_request

try:
    from threading import local
except ImportError:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from django.utils._threading_local import local

_thread_locals = local()


class CustomHttpHandler(HTTPHandler):
    def __init__(self, filename, host, url, method):
        HTTPHandler.__init__(self, host, url, method)
        self.logPath = filename
        self.session = requests.Session()

    def mapLogRecord(self, record):
        record_modified = super().mapLogRecord(record)
        record_modified['logPath'] = self.logPath
        if getattr(record, 'request_id', None):
            record_modified['msg'] = '{} | {}'.format(record.request_id, self.format(record))
        else:
            record_modified['msg'] = self.format(record)
        return record_modified

    def emit(self, record):
        try:
            url = 'http://' + self.host + '/' + self.url
            data = self.mapLogRecord(record)

            self.session.post(url, data=data, timeout=10)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def add_custom_attribute_filter(record):
    try:
        x_traceid = get_current_request().META.get('HTTP_X_TRACEID')  # set by proxy server (nginx)
    except AttributeError:
        x_traceid = None

    if not x_traceid:
        x_traceid = getattr(_thread_locals, '__request__x_traceid', None)  # generate traceid for request
        if not x_traceid:
            import uuid
            x_traceid = uuid.uuid4().hex
            _thread_locals.__request__x_traceid = x_traceid

    record.request_id = x_traceid

    return True


main = getLogger('main')
