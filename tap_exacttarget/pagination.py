import datetime
import singer

from tap_exacttarget.filters import between

LOGGER = singer.get_logger()
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def before_now(date_value):
    return (datetime.datetime.strptime(date_value, DATE_FORMAT) <=
            datetime.datetime.utcnow())


def increment_date(date_value, unit=None):
    if unit is None:
        unit = {'days': 1}

    date_obj = datetime.datetime.strptime(date_value, DATE_FORMAT)

    incremented_date_obj = date_obj + datetime.timedelta(**unit)
    now = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)

    if incremented_date_obj < now:
        str_date = datetime.datetime.strftime(incremented_date_obj, DATE_FORMAT)
        exceeded = False
    else:
        str_date = datetime.datetime.strftime(now, DATE_FORMAT)
        exceeded = True

    return str_date, exceeded


def get_date_page(field, start, unit):
    return between(field, start, increment_date(start, unit)[0])
