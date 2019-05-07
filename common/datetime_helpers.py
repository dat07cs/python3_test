import calendar
import datetime
import re
import time
from datetime import datetime, timedelta

import pytz
from django.utils import timezone


class TimeUtils(object):
    TIMEZONE = 'Asia/Ho_Chi_Minh'
    try:
        from django.conf import settings
        TIMEZONE = settings.TIME_ZONE
    except:
        pass

    ONE_SECOND_DELTA = timedelta(seconds=1)
    ONE_MINUTE_DELTA = timedelta(minutes=1)
    ONE_HOUR_DELTA = timedelta(hours=1)
    ONE_DAY_DELTA = timedelta(days=1)

    ONE_MINUTE_SECONDS = int(ONE_MINUTE_DELTA.total_seconds())
    ONE_HOUR_SECONDS = int(ONE_HOUR_DELTA.total_seconds())
    ONE_DAY_SECONDS = ONE_HOUR_SECONDS * 24
    ONE_WEEK_SECONDS = ONE_DAY_SECONDS * 7

    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def get_tz(cls, country_code):
        try:
            return pytz.country_timezones(country_code)[0]
        except:
            return cls.TIMEZONE

    @classmethod
    def get_pytz_timezone(cls, tz, country_code):
        if tz is None:
            tz = cls.TIMEZONE

        if country_code:
            tz = cls.get_tz(country_code)

        return pytz.timezone(tz)

    @classmethod
    def datetime_to_ts(cls, dt, tz=None, country_code=None):
        if dt and dt.tzinfo is None:
            tz = cls.get_pytz_timezone(tz, country_code)
            dt = tz.localize(dt)

        return calendar.timegm(dt.utctimetuple()) if dt else None

    @classmethod
    def datetime_to_str(cls, dt, dt_format=DATE_FORMAT, tz=None, country_code=None):
        tz = cls.get_pytz_timezone(tz, country_code)
        if dt and dt.tzinfo is None:
            dt = tz.localize(dt)

        return dt.strftime(dt_format)

    @classmethod
    def ts_to_datetime(cls, timestamp, tz=None, country_code=None):
        utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
        tz = cls.get_pytz_timezone(tz, country_code)
        return tz.normalize(utc_dt.astimezone(tz))

    @classmethod
    def ts_to_str(cls, timestamp, dt_format=DATE_FORMAT, tz=None, country_code=None):
        dt_tz = cls.ts_to_datetime(timestamp, tz, country_code)
        return dt_tz.strftime(dt_format)

    @classmethod
    def str_to_datetime(cls, date_str, dt_format=DATE_FORMAT, tz=None, country_code=None):
        tz = cls.get_pytz_timezone(tz, country_code)
        return tz.localize(datetime.strptime(date_str, dt_format))

    @classmethod
    def str_to_ts(cls, date_str, dt_format=DATE_FORMAT, tz=None, country_code=None):
        dt = cls.str_to_datetime(date_str, dt_format, tz, country_code)
        return calendar.timegm(dt.utctimetuple()) if dt else None

    @classmethod
    def date_to_datetime(cls, date_, tz=None, country_code=None):
        utc_ts = calendar.timegm(date_.timetuple())
        utc_dt = datetime.utcfromtimestamp(utc_ts)

        tz = cls.get_pytz_timezone(tz, country_code)
        return tz.localize(utc_dt)

    @classmethod
    def date_to_ts(cls, date_, tz=None, country_code=None):
        dt_tz = cls.date_to_datetime(date_, tz, country_code)
        return cls.datetime_to_ts(dt_tz, tz, country_code)

    @classmethod
    def date_to_str(cls, date_, dt_format=DATE_FORMAT, tz=None, country_code=None):
        dt_tz = cls.date_to_datetime(date_, tz, country_code)
        return cls.datetime_to_str(dt_tz, dt_format, tz, country_code)

    @classmethod
    def set_datetime_tz(cls, dt, tz=None, country_code=None):
        tz = cls.get_pytz_timezone(tz, country_code)
        return dt.astimezone(tz)

    @classmethod
    def now_timestamp(cls, in_real=False):
        now = time.time()
        if not in_real:
            now = int(now)

        return now

    @classmethod
    def today(cls, dt_format=DATE_FORMAT, tz=None, country_code=None):
        utc_dt = datetime.utcnow().replace(tzinfo=pytz.utc)
        tz = cls.get_pytz_timezone(tz, country_code)
        dt_tz = tz.normalize(utc_dt.astimezone(tz))

        if not dt_format:
            return dt_tz

        return dt_tz.strftime(dt_format)

    @classmethod
    def round_datetime(cls, datetime_obj, tz=None, country_code=None):
        tz = cls.get_pytz_timezone(tz, country_code)
        dt_tz = tz.normalize(datetime_obj)
        dt_tz = dt_tz.replace(hour=0, minute=0, second=0, microsecond=0)

        return dt_tz

    @classmethod
    def round_ts(cls, timestamp=None, tz=None, country_code=None):
        if timestamp is None:
            timestamp = cls.now_timestamp()

        utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
        dt_tz = cls.round_datetime(utc_dt, tz, country_code)
        return calendar.timegm(dt_tz.utctimetuple())

    # http://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string#answer-4628148
    _TIME_DELTA_STR_REGEX = re.compile(
        r"[ ]*"
        r"((?P<days>\d+?)d)?[ ]*"
        r"((?P<hours>\d+?)h)?[ ]*"
        r"((?P<minutes>\d+?)m)?[ ]*"
        r"((?P<seconds>\d+?)s)?"
        r"[ ]*"
    )

    @classmethod
    def parse_timedelta(cls, time_delta_str, to_int=False):
        """
        Convert from `timedelta` string to seconds.

        Examples:
        - "1d12h30m" => timedelta(days=1, hours=12, minutes=30)
        - "2h15m30s" => timedelta(hours=2, minutes=15, seconds=30)

        :param to_int:
        :param time_delta_str: Support these formats:
        - d: days
        - h: hours
        - m: minutes
        - s: seconds
        """
        parts = cls._TIME_DELTA_STR_REGEX.match(time_delta_str)
        if not parts:
            return timedelta()

        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)

        delta = timedelta(**time_params)
        if to_int:
            return int(delta.total_seconds())

        return delta

    @classmethod
    def get_nearest_past_datetime_by_day(cls, day, date_obj=None):
        if not date_obj:
            # noinspection PyTypeChecker
            date_obj = cls.today(dt_format=None)

        if date_obj.day >= day:
            return date_obj.replace(day=day)

        begin_month_date = date_obj.replace(day=1)
        prev_month_date = begin_month_date - timedelta(days=1)
        return prev_month_date.replace(day=day)


def today_is_dow(int_dow_value, django_timezone=True):
    if django_timezone:
        return int_dow_value == timezone.localtime(timezone.now()).weekday()
    return datetime.today().weekday()


def get_current_tzdatetime():
    return timezone.localtime(timezone.now())


def string_to_tzdatetime(datetime_str, format_str):
    tz = timezone.get_current_timezone()
    dt = tz.localize(datetime.datetime.strptime(datetime_str, format_str))
    return dt


def tzdatetime_to_timestamp(dt):
    return int(time.mktime(dt.timetuple()))


def timestamp_to_tzdatetime(ts):
    tz = timezone.get_current_timezone()
    dt = datetime.datetime.fromtimestamp(ts, tz)
    return dt


def tzdatetime_to_string(tzdatetime, format_str):
    return tzdatetime.strftime(format_str)


def tzdatetime_to_localtime_string(tzdatetime, format_str):
    return timezone.localtime(tzdatetime).strftime(format_str)
