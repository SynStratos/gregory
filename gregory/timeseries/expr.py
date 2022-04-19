from datetime import datetime

from ..dataclass.time_series_data import TimeSeriesData
from ..timeseries.time_series import TimeSeries
from ..util.dictionaries import merge_with_conflict


def intersection(tsl_a: TimeSeries, tsl_b: TimeSeries) -> TimeSeries:
    """
    Given two input time series, generates a new time series with only shared 
    days and all the contained values.

    Args:
        tsl_a (TimeSeries): First input time series.
        tsl_b (TimeSeries): Second input time series.

    Returns:
        TimeSeries: Output timeseries with shared days.
    """
    intersection_dates = tsl_a.__indexes__.keys() & tsl_b.__indexes__.keys()
    return TimeSeries(
        [
            TimeSeriesData(
                day=datetime.strptime(day, "%Y-%m-%d"),
                series=merge_with_conflict(
                    tsl_a.get(datetime.strptime(day, "%Y-%m-%d")).series,
                    tsl_b.get(datetime.strptime(day, "%Y-%m-%d")).series
                )
            ) for day in intersection_dates
        ]
    )


def union(tsl_a: TimeSeries, tsl_b: TimeSeries) -> TimeSeries:
    """
    Given two input time series, generates a new time series with the union of 
    all days of both series.

    Args:
        tsl_a (TimeSeries): First input time series.
        tsl_b (TimeSeries): Second input time series.

    Returns:
        TimeSeries: Output timeseries with all days.
    """
    union_dates = tsl_a.__indexes__.keys() | tsl_b.__indexes__.keys()

    return TimeSeries(
        [
            TimeSeriesData(
                day=datetime.strptime(day, "%Y-%m-%d"),
                series=merge_with_conflict(
                    tsl_a.get_series_or_empty(
                        datetime.strptime(day, "%Y-%m-%d")),
                    tsl_b.get_series_or_empty(
                        datetime.strptime(day, "%Y-%m-%d"))
                )
            ) for day in union_dates
        ]
    )


def merge(tsl_a: TimeSeries, tsl_b: TimeSeries, method) -> TimeSeries:
    raise NotImplementedError
