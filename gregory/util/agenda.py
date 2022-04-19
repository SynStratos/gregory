import calendar
from datetime import date, datetime, timedelta
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR, SA, SU
import numpy as np

from .decorators import day_or_datetime
from ..util.relativedelta import relativedelta

WEEKMASK = [
    [1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1]
]

WEEKDAYS = [MO, TU, WE, TH, FR, SA, SU]

weekday_assertion_msg = "Weekday must be between 1 and 7."


@day_or_datetime
def get_quarter(day: date) -> int:
    """
    Searches the quarter of the year that includes the given day.
    Possible outputs are 1, 2, 3, 4.
    """
    return (day.month - 1) // 3 + 1


@day_or_datetime
def first_day_of_week(day: date) -> date:
    """Searches the first day of the week that includes the given day."""
    return day - relativedelta(days=day.weekday())


@day_or_datetime
def last_day_of_week(day: date) -> date:
    """Searches the last day of the week that includes the given day."""
    return day + relativedelta(days=6 - day.weekday())


@day_or_datetime
def first_day_of_month(day: date) -> date:
    """Searches the first day of the month that includes the given day."""
    return day.replace(day=1)


@day_or_datetime
def last_day_of_month(day: date) -> date:
    """Searches the last day of the month that includes the given day."""
    return day.replace(day=days_of_month(day=day))


@day_or_datetime
def first_day_of_quarter(day: date) -> date:
    """Searches the first day of the quarter that includes the given day."""
    quarter = get_quarter(day)
    return datetime(year=day.year, month=3 * quarter - 2, day=1).date()


@day_or_datetime
def last_day_of_quarter(day: date) -> date:
    """Searches the last day of the quarter that includes the given day."""
    quarter = get_quarter(day)
    return datetime(
        year=day.year + 3 * quarter // 12,
        month=3 * quarter % 12 + 1,
        day=1
    ).date() + timedelta(days=-1)


@day_or_datetime
def first_day_of_year(day: date) -> date:
    """Searches the first day of the year that includes the given day."""
    return day.replace(month=1, day=1)


@day_or_datetime
def last_day_of_year(day: date) -> date:
    """Searches the last day of the year that includes the given day."""
    return day.replace(month=12, day=31)


@day_or_datetime
def days_of_month(day: date) -> int:
    """Returns the length of the month containing the day, expressed in days."""
    return calendar.monthrange(day.year, day.month)[1]


@day_or_datetime
def days_of_quarter(day: date) -> int:
    """
    Returns the length of the quarter containing the day, expressed in days.
    """
    first_day = first_day_of_quarter(day)
    last_day = last_day_of_quarter(day)
    return (last_day - first_day).days


@day_or_datetime
def days_of_year(day: date) -> int:
    """Returns the length of the year containing the day, expressed in days."""
    return 365 + calendar.isleap(day.year)


def weekdays_of_range(start_date: date, end_date: date, weekday: int, exclusive: bool = False):
    assert 1 <= weekday <= 7, weekday_assertion_msg
    day_times = rrule(
        freq=DAILY,
        dtstart=start_date,
        until=end_date + relativedelta(days=int(exclusive)),
        byweekday=(WEEKDAYS[weekday-1])
    )
    days = [day_time.date() for day_time in day_times]
    n_days = len(days)
    return n_days, days


def calendar_by_steps(start_date: date, end_date: date, step: relativedelta) -> list:
    """
    Evaluates steps between start_date and end_date.

    Args:
        start_date (date): First date of the period.
        end_date (date): Last date of the period.
        step (relativedelta): Time step.

    Returns:
        list: Time range dates with a defined step.
    """

    assert end_date > start_date, "end date must be greater than start date"

    res = []
    while start_date <= end_date:
        res.append(
            start_date
        )
        start_date += step

    return res
