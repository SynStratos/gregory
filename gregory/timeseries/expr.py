from functools import reduce
from typing import List, Callable, Any, Dict

from outatime.timeseries.expr import union as union_, intersection as intersection_
from gregory.timeseries.time_series import TimeSeries
from gregory.dataclass.time_series_data import TimeSeriesData
from gregory.util.decorators import as_gregory_ts


@as_gregory_ts
def union(tsl_a: TimeSeries, tsl_b: TimeSeries, conflict_method: Callable[[Dict, Dict], Dict]) -> TimeSeries:
    return union_(tsl_a, tsl_b, conflict_method)


@as_gregory_ts
def intersection(tsl_a: TimeSeries, tsl_b: TimeSeries, conflict_method: Callable[[Dict, Dict], Dict]) -> TimeSeries:
    return intersection_(tsl_a, tsl_b, conflict_method)


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


def list_intersection(ts_list: List[TimeSeries], conflict_method: Callable[[List[Dict]], Dict]) -> TimeSeries:
    """
    Given a list of time series, generates a new time series with only shared
    days and all the contained values.

    Args:
        ts_list (List[TimeSeries]): Input list of time series.
        conflict_method (Callable[[List[Dict]], Dict]): Method to apply
        when choosing data for matching days.

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


def list_union(ts_list: List[TimeSeries], conflict_method: Callable[[List[Dict]], Dict]) -> TimeSeries:
    """
    Given a list of time series, generates a new time series with the union of
    all days of both series.

    Args:
        ts_list (List[TimeSeries]): Input list of time series.
        conflict_method (Callable[[List[Dict]], Dict]): Method to apply
        when choosing data for matching days.

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
