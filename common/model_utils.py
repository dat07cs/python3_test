import binascii
from datetime import datetime

from django.db import models, connections, transaction
from django.db.models import BigIntegerField, AutoField

from common import utility_helpers


class BigForeignKey(models.ForeignKey):
    def db_type(self, connection):
        """ Adds support for foreign keys to big integers as primary keys.
        """
        rel_field = self.rel.get_related_field()
        if (isinstance(rel_field, BigAutoField) or
                (not connection.features.related_fields_match_type and
                 isinstance(rel_field, (BigIntegerField,)))):
            return BigIntegerField().db_type(connection=connection)
        return super(BigForeignKey, self).db_type(connection)


class PositiveBigIntegerField(BigIntegerField):
    empty_strings_allowed = False

    def db_type(self, connection):
        return "bigint UNSIGNED"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': BigIntegerField.MAX_BIGINT * 2 - 1}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)


class BigAutoField(AutoField):
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'bigint UNSIGNED AUTO_INCREMENT'
        return super(BigAutoField, self).db_type(connection)

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': BigIntegerField.MAX_BIGINT * 2 - 1}
        defaults.update(kwargs)
        return super(BigAutoField, self).formfield(**defaults)


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        return "tinyint"

    def formfield(self, **kwargs):
        defaults = {'min_value': -128, 'max_value': 127}
        defaults.update(kwargs)
        return super(TinyIntegerField, self).formfield(**defaults)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        return "tinyint unsigned"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': 255}
        defaults.update(kwargs)
        return super(PositiveTinyIntegerField, self).formfield(**defaults)


class Counter(models.Model):
    name = models.CharField(max_length=32, unique=True)
    sequence = models.BigIntegerField(default=1)


# Common Sharding Functions:
def shard_by_datetime(dt_format):
    def func(timestamp):
        return datetime.fromtimestamp(int(timestamp)).strftime(dt_format)

    return staticmethod(func)


def shard_by_crchash(base):
    def func(s):
        return binascii.crc32(s) % base

    return staticmethod(func)


def shard_by_mod(base):
    def func(n):
        return n % base

    return staticmethod(func)


def model_get_optional_result(func):
    def _func(*args, **kwargs):
        results = func(*args, **kwargs)
        if not results:
            return None
        return results[0]

    return _func


def copy_model_object(obj):
    data = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields])
    return utility_helpers.dict_to_object(data)  # fixme


def copy_model_list(l):
    return [copy_model_object(v) for v in l]


def call_sp(using='default', sp_name='', args=()):
    cur = connections[using].cursor()
    query = 'call %s(%s);' % (sp_name, ','.join(['%s'] * len(args)))
    cur.execute(query, args)
    return cur.fetchall()


def call_sp_fetch_one(using='default', sp_name='', args=()):
    cur = connections[using].cursor()
    query = 'call %s(%s);' % (sp_name, ','.join(['%s'] * len(args)))
    cur.execute(query, args)
    return cur.fetchone()


def increase_counter(name):
    with transaction.atomic():
        to_update = models.Counter.objects.filter(name=name)
        affected = to_update.update(sequence=F('sequence') + 1)
        if affected:
            return models.Counter.objects.get(name=name).sequence

    _, created = models.Counter.objects.get_or_create(name=name)
    if created:
        return 1

    with transaction.atomic():
        to_update.update(sequence=F('sequence') + 1)
        return models.Counter.objects.get(name=name).sequence