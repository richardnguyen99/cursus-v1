# -*- coding: utf-8 -*-

"""Datetime utility module for working with datetime objects
"""

import datetime

from typing import Optional


def datetime_until_end_of_day(
    dt: Optional[datetime.datetime] = None,
) -> datetime.timedelta:
    """
    Get the remaining time until the end of the current day.

    If `dt` is `None`, or not specified, `datetime.datetime.now()` is used.

    :param dt: datetime object to use for the calculation
    :return: timedelta object representing the remaining time until the end of
            the day
    """

    if dt is None:
        dt = datetime.datetime.now()

    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min) - dt
