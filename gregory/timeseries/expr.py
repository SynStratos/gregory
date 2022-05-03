from functools import reduce
from typing import List

from outatime.timeseries.expr import *


def first_or_empty(_list: list):
    _list = [_el for _el in _list if _el]
    try:
        return _list[0]
    except IndexError:
        return {}


def list_intersection(ts_list: List[TimeSeries], conflict_method=first_or_empty) -> TimeSeries:
    dates_list = [ts.dates for ts in ts_list]
    intersection_dates = list(reduce(lambda x, y: set(x) & set(y), dates_list))
    intersection_dates.sort()

    intersection_result = []
    for int_date in intersection_dates:
        intersection_result.append(
            TimeSeriesData(
                day=int_date,
                data=conflict_method([tsl.get(day=int_date).data for tsl in ts_list])
            )
        )
    return TimeSeries(intersection_result)


def list_union(ts_list: List[TimeSeries], conflict_method=first_or_empty) -> TimeSeries:
    dates_list = [ts.dates for ts in ts_list]
    union_dates = list(reduce(lambda x, y: set(x) | set(y), dates_list))
    union_dates.sort()

    union_result = []
    for uni_date in union_dates:
        union_result.append(
            TimeSeriesData(
                day=uni_date,
                data=conflict_method([tsl.get(day=uni_date).data for tsl in ts_list])
            )
        )
    return TimeSeries(union_result)
