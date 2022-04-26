from copy import copy
from typing import List
from ..dataclass.time_series_data import TimeSeriesData
from ..granularity.granularity import Granularity, WeeklyGranularity
from ..granularity.utils import get_first_available_beginning
from ..timeseries.time_series import TimeSeries
from ..util.dictionaries import aggregate_dicts
from ..util.bisect import *


def batches(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        first_day_of_batch: int = 0,
        n_elements: int = -1
) -> List[TimeSeries]:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to WeeklyGranularity().
        first_day_of_batch (int, optional): The day of the time step to use as 
        first delimiter (0-indexed). Defaults to 0.
        n_elements (int, optional): The length of the sub-set of the time step 
        to use. Defaults to -1.

    Returns:
        List[TimeSeries]: A list of small time series.
    """
    assert n_elements > 0 or n_elements == - \
        1, "'n_elements' must be greater than 0 or set to -1 to get all elements."
    assert first_day_of_batch >= 0, "'first_day_of_batch' can't be lesser than 0."

    res = []

    # def next_day
    fst_av_beg = get_first_available_beginning(
        day=ts.start_date,
        input_granularity=ts.data_granularity,
        output_granularity=granularity
    )
    f_day = granularity.get_n_day_of_granularity(fst_av_beg, first_day_of_batch)

    temp_ts = ts.__deepcopy__()

    while f_day <= ts.end_date:
        if n_elements > 0:
            l_day = granularity.get_n_day_of_granularity(
                day=f_day, idx=n_elements-1)
        else:
            l_day = granularity.get_end_of_granularity(day=f_day)

        idx_min, idx_max = find_delimiters(temp_ts.dates, f_day, l_day)

        res.append(
            temp_ts[idx_min:idx_max]
        )

        temp_ts = temp_ts[idx_max:]
        fst_av_beg += granularity.delta
        f_day = granularity.get_n_day_of_granularity(fst_av_beg, first_day_of_batch)

    return res


def aggregate_on_first_day(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        method=sum,
        first_day_of_batch: int = 0,
        n_elements: int = -1,
        on_last_day: bool = False
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity. Then aggregates each sub-set data into a single 
    TimeSeriesData to generate a new TimeSeries output.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to WeeklyGranularity().
        method (optional): Aggregation function. Defaults to sum.
        first_day_of_batch (int, optional): The day of the time step to use as 
        first delimiter (0-indexed). Defaults to 0.
        n_elements (int, optional): The length of the sub-set of the time step 
        to use. Defaults to -1.
        on_last_day (bool, optional): Aggregate on the last day instead of the
        first one. Defaults to False.

    Returns:
        TimeSeries: A new time series with aggregated values.
    """
    assert n_elements > 0 or n_elements == - \
        1, "'n_elements' must be greater than 0 or set to -1 to get all elements."
    assert first_day_of_batch >= 0, "'first_day_of_batch' can't be lesser than 0."

    res = []

    fst_av_beg = get_first_available_beginning(day=ts.start_date, input_granularity=ts.data_granularity, output_granularity=granularity)
    f_day = granularity.get_n_day_of_granularity(fst_av_beg, idx=first_day_of_batch)

    temp_ts = ts.__deepcopy__()

    while f_day <= ts.end_date:
        if n_elements > 0:
            l_day = granularity.get_n_day_of_granularity(
                day=f_day, idx=n_elements-1)
        else:
            l_day = granularity.get_end_of_granularity(day=f_day)

        idx_min, idx_max = find_delimiters(temp_ts.dates, f_day, l_day)

        aggregate_series = aggregate_dicts(
            [element.series for element in temp_ts[idx_min:idx_max]], method=method)

        res.append(
            TimeSeriesData(
                day=l_day if on_last_day else f_day,
                series=aggregate_series
            )
        )

        temp_ts = temp_ts[idx_max:]
        fst_av_beg += granularity.delta
        f_day = granularity.get_n_day_of_granularity(fst_av_beg, idx=first_day_of_batch)

    return TimeSeries(res)


def pick_a_day(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        day_of_batch: int = -1
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity. Then returns a new TimeSeries with only the n-th
    day of each batch.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to WeeklyGranularity().
        day_of_batch (int, optional): The day of the time step to pick as 
        reference (0-indexed). Defaults to -1.

    Returns:
        TimeSeries: A new time series with only a day for each step.
    """
    assert day_of_batch >= -1, "'day_of_batch' can't be lesser than -1."

    res = []
    fst_av_beg = get_first_available_beginning(
        day=ts.start_date,
        input_granularity=ts.data_granularity,
        output_granularity=granularity
    )
    f_day = granularity.get_n_day_of_granularity(fst_av_beg, day_of_batch)

    while f_day <= ts.end_date:
        res.append(
            copy(ts.get(day=f_day, else_empty=True))
        )

        fst_av_beg += granularity.delta
        f_day = granularity.get_n_day_of_granularity(fst_av_beg, day_of_batch)

    return TimeSeries(res)


def pick_a_weekday(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        day_of_batch: int = -1,
        weekday: int = 1
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step
    of the given granularity. Then returns a new TimeSeries with only the n-th 
    chosen day of the week of each batch.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the
        input series. Defaults to WeeklyGranularity().
        day_of_batch (int, optional): The weekday of the time step to pick as 
        reference (0-indexed). Defaults to -1.
        weekday (int, optional): The day of the time step to use as
        first delimiter (1-indexed). Defaults to 1.

    Returns:
        TimeSeries: A new time series with only a day for each step.
    """
    assert day_of_batch >= -1, "'day_of_batch' can't be lesser than -1."

    res = []
    fst_av_beg = get_first_available_beginning(
        day=ts.start_date,
        input_granularity=ts.data_granularity,
        output_granularity=granularity
    )
    f_day = granularity.get_n_weekday_of_granularity(day=fst_av_beg, weekday=weekday, idx=day_of_batch)

    while f_day <= ts.end_date:
        res.append(
            copy(ts.get(day=f_day, else_empty=True))
        )

        fst_av_beg += granularity.delta
        f_day = granularity.get_n_weekday_of_granularity(day=fst_av_beg, weekday=weekday, idx=day_of_batch)

    return TimeSeries(res)
