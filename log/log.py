import datetime as d
from .. import utility as u


def time_string2datetime(time_string):
    date_tmp = d.datetime.strptime(time_string, '%Y%j%H%M%S')
    return d.datetime(
        date_tmp.year,
        date_tmp.month,
        date_tmp.day,
        date_tmp.hour,
        date_tmp.minute,
        date_tmp.second,
        tzinfo=u.utc_timezone())


def datetime2doy_string(time):
    return time.strftime('%Y%j')


def datetime2time_string(time):
    return time.strftime('%Y%j%H%M%S')
