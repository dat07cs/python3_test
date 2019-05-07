# coding: utf-8

# https://github.com/jedie/django-tools/blob/master/django_tools/middlewares/ThreadLocal.py

from __future__ import absolute_import, division, print_function

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object  # fallback for Django < 1.10


_thread_locals = local()


def get_current_request():
    """ returns the request object for this thread """
    return getattr(_thread_locals, "request", None)


class ThreadLocalMiddleware(MiddlewareMixin):
    """ Simple middleware that adds the request object in thread local storage."""
    def process_request(self, request):
        _thread_locals.request = request

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response

    def process_exception(self, request, exception):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
