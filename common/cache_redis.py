import json
from functools import wraps

import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
NS = 'default-ns'
ALL_KEYS_MATCHER = NS + ':*'


def using_cache(cache_prefix, is_json=True):
    def _decorator(func):
        @wraps(func)
        def _wrap(self, *args, **kwargs):
            try:
                cache_key = build_cache_key(cache_prefix, *args, **kwargs)
                cache_value = r.get(cache_key)
                if cache_value is None:
                    cache_value = func(self, *args, **kwargs)
                    cache_value = json.dumps(cache_value) if is_json is True else cache_value
                    r.set(cache_key, cache_value)
                return json.loads(cache_value) if is_json is True else cache_value
            except:
                return func(self, *args, **kwargs)
        return _wrap
    return _decorator


def build_cache_key(prefix, *args, **kwargs):
    cache_key_list = [NS, prefix]
    if len(args):
        cache_key_list.append('-'.join([str(item)for item in args]))
    if len(kwargs):
        cache_key_list.append(str(kwargs))
    return ':'.join(cache_key_list)


def get_all_cache():
    return ['%s:%s' % (key, r.get(key)) for key in r.scan_iter(ALL_KEYS_MATCHER)]


def clear_all_cache():
    for key in r.scan_iter(ALL_KEYS_MATCHER):
        r.delete(key)


def get_cache_by_key(key):
    return r.get(key)


def save_cache(key, value, expired_second=None):
    r.set(key, value, ex=expired_second)
