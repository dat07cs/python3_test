import functools
import inspect
import timeit
from typing import Optional

import requests
from django.conf import settings
from requests import Response
from rest_framework.request import Request

from common import json_helpers
from common.logger import main as logger


def get_request_data(request: Request) -> dict:
    if request.method == 'GET':
        data = request.query_params
    else:  # request.method == 'POST'
        data = request.data
    return data


def _safe_dumps(obj):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return json_helpers.json_compact_dumps(obj)
    return str(obj)


def decorator_timeit(func):
    @functools.wraps(func)
    def wrapper(url, *args, **kwargs):
        start = timeit.default_timer()
        result = func(url, *args, **kwargs)
        end = timeit.default_timer()
        logger.info('method=%s, url=%s, elapsed_time=%.3fs', func.__name__, url, end - start)
        return result
    return wrapper


def decorator_logging(func):
    @functools.wraps(func)
    def api_wrapper(url, timeout=settings.DEFAULT_SERVICE_TIMEOUT, **kwargs):
        caller_frame_info = inspect.getframeinfo(inspect.currentframe().f_back)
        caller = '%s.%s' % (caller_frame_info.filename.split('/')[-1][:-3], caller_frame_info.function)
        level = logger.INFO
        response = None
        kwargs.setdefault('timeout', timeout)
        try:
            response = func(url, **kwargs)  # type: Optional[Response]
            return response
        except:
            level = logger.ERROR
            raise
        finally:
            request = '{} {} {}'.format(func.__name__.upper(), url,
                                        _safe_dumps(kwargs.get('params') or kwargs.get('data') or kwargs.get('json')))
            reply = '{} {}'.format(response, response.text) if response is not None else None
            logger.log(level, 'caller=%s, request=%s, reply=%s', caller, request, reply, exc_info=0)
    return api_wrapper


get = decorator_logging(decorator_timeit(requests.get))
post = decorator_logging(decorator_timeit(requests.post))
