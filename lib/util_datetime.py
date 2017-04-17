import datetime
import pytz


def tzware_datetime():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    return datetime.datetime.now(pytz.utc)


def timedelta(days=0, hours=0, minutes=0, compare_date=None):
    """
    Return a new datetime with a offset applied.

    :param days: Amount of days to offset
    :type days: int
    :param hours: Amount of hours to offset
    :type hours: int
    :param minutes: Amount of days to offset
    :type minutes: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = tzware_datetime()

    compare_date_with_delta = compare_date + datetime.timedelta(days=days, hours=hours, minutes=minutes)

    return compare_date_with_delta


def timedelta_months(months, compare_date=None):
    """
    Return a new datetime with a month offset applied.

    :param months: Amount of months to offset
    :type months: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = datetime.date.today()

    delta = months * 365 / 12
    compare_date_with_delta = compare_date + datetime.timedelta(delta)

    return compare_date_with_delta
