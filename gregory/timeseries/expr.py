from functools import reduce
from typing import List

from outatime.timeseries.expr import *


def first_or_empty(list_: list):
    list_ = [_el for _el in list_ if _el]
    try:
        return list_[0]
    except IndexError:
        return {}


def get_list_of_dates(ts_list: List[TimeSeries]) -> list:
    """
    Given a list of TimeSeries, returns a list of their dates
    attributes.

    Args:
        ts_list (List[TimeSeries]): Input list of Time Series.

    Returns:
        list: List of dates lists.
    """
    return [ts.dates for ts in ts_list]


def intersection_dates(dates: list) -> list:
    """
    Returns common dates between elements of a list of dates
    list.

    Args:
        dates (list): List of dates lists.

    Returns:
        list: List of common dates.
    """
    _intersection_dates = list(reduce(lambda x, y: set(x) & set(y), dates))
    _intersection_dates.sort()
    return _intersection_dates


def union_dates(dates: list) -> list:
    """
    Returns all dates present in elements of a list of dates
    list.

    Args:
        dates (list): List of dates lists.

    Returns:
        list: List of all dates (each taken once).
    """
    _union_dates = list(reduce(lambda x, y: set(x) | set(y), dates))
    _union_dates.sort()
    return _union_dates


def list_intersection(ts_list: List[TimeSeries], conflict_method=first_or_empty) -> TimeSeries:
    """
    Given a list of time series, generates a new time series with only shared
    days and all the contained values.

    Args:
        ts_list (List[TimeSeries]): Input list of time series.
        conflict_method (None, optional): Method to apply when choosing
        data for matching days. Defaults to first_or_empty.

    Returns:
        TimeSeries: Output timeseries with shared days.
    """
    dates_list = get_list_of_dates(ts_list)
    int_dates = intersection_dates(dates_list)

    intersection_result = []
    for int_date in int_dates:
        intersection_result.append(
            TimeSeriesData(
                day=int_date,
                data=conflict_method([tsl.get(day=int_date).data for tsl in ts_list])
            )
        )
    return TimeSeries(intersection_result)


def list_union(ts_list: List[TimeSeries], conflict_method=first_or_empty) -> TimeSeries:
    """
    Given a list of time series, generates a new time series with the union of
    all days of both series.

    Args:
        ts_list (List[TimeSeries]): Input list of time series.
        conflict_method (None, optional): Method to apply when choosing
        data for matching days. Defaults to first_or_empty.

    Returns:
        TimeSeries: Output timeseries with all days.
    """
    dates_list = get_list_of_dates(ts_list)
    uni_dates = union_dates(dates_list)

    union_result = []
    for uni_date in uni_dates:
        union_result.append(
            TimeSeriesData(
                day=uni_date,
                data=conflict_method([tsl.get(day=uni_date).data for tsl in ts_list])
            )
        )
    return TimeSeries(union_result)
