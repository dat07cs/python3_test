import functools

from django.core.cache import caches
from django.core.cache.backends.memcached import MemcachedCache

memcached = caches['memcached']  # type: MemcachedCache


def decorator_cache(cache_key, timeout=None):
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = memcached.get(cache_key)
            if not result:
                result = func(*args, **kwargs)
                ttl = timeout or memcached.get_backend_timeout()
                memcached.set(cache_key, result, timeout=ttl)
            return result
        return wrapper
    return real_decorator


def decorator_cache_based_on_id(prefix, timeout=None):
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(index):
            cache_key = '{}_{}'.format(prefix, str(index))
            result = memcached.get(cache_key)
            if not result:
                result = func(index)
                ttl = timeout or memcached.get_backend_timeout()
                memcached.set(cache_key, result, timeout=ttl)
            return result
        return wrapper
    return real_decorator
