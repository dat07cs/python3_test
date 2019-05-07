import json

import decimal

import datetime
from django.utils import timezone


class ExtendedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            if timezone.is_aware(obj):
                obj = timezone.localtime(obj)
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


def json_compact_dumps(params, sort_keys=True, ensure_ascii=True, **kwargs):
    return json.dumps(params, separators=(',', ':'), cls=ExtendedJsonEncoder,
                      sort_keys=sort_keys, ensure_ascii=ensure_ascii, **kwargs)


def safe_loads(json_string):
    try:
        return json.loads(json_string)
    except (TypeError, ValueError):
        return {}


def _serialize_value(obj):
    try:
        ret_dict = obj.__dict__
    except:
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            if timezone.is_aware(obj):
                obj = timezone.localtime(obj)
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')

        raise TypeError(repr(obj) + " is not JSON serializable")

    return ret_dict


def object_to_json(obj):
    json_str = json.dumps(obj, ensure_ascii=False, separators=(',', ':'), default=lambda o: _serialize_value(o),
                          sort_keys=False, indent=4)
    return json.loads(json_str)


_slash_escape = '\\/' in json_compact_dumps('/')


def to_json_html_safe(obj, **kwargs):
    rv = json_compact_dumps(obj, **kwargs) \
        .replace(u'<', u'\\u003c') \
        .replace(u'>', u'\\u003e') \
        .replace(u'&', u'\\u0026') \
        .replace(u"'", u'\\u0027') \
        .replace(u'\u2028', u'\\u2028') \
        .replace(u'\u2029', u'\\u2029')
    if _slash_escape:
        rv = rv.replace('\\/', '/')
    return rv
