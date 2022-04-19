from typing import List
from ..dataclass.time_series_data import TimeSeriesData
from ..granularity.granularity import Granularity, DailyGranularity
from ..timeseries.time_series import TimeSeries
from ..util.dictionaries import aggregate_dicts
from ..util.bisect import *


def batches(
        ts: TimeSeries,
        granularity: Granularity = DailyGranularity(),
        first_day_of_batch: int = 1,
        n_elements: int = -1
) -> List[TimeSeries]:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to DailyGranularity().
        first_day_of_batch (int, optional): The day of the time step to use as 
        first delimiter. Defaults to 1.
        n_elements (int, optional): The length of the sub-set of the time step 
        to use. Defaults to 0.

    Returns:
        List[TimeSeries]: A list of small time series.
    """
    assert n_elements > 0 or n_elements == - \
        1, "'n_elements' must be greater than 0 or set to -1 to get all elements."
    assert first_day_of_batch >= 1, "'first_day_of_batch' can't be lesser than 1."

    res = []

    fst_av_beg = granularity.get_first_available_beginning(day=ts.start_date)
    f_day = granularity.get_n_day_of_granularity(
        fst_av_beg, first_day_of_batch)

    temp_ts = ts.__deepcopy__()

    while f_day <= ts.end_date:
        if n_elements > 0:
            l_day = granularity.get_n_day_of_granularity(
                day=f_day, n=n_elements)
        else:
            l_day = granularity.get_end_of_granularity(day=f_day)

        idx_min, idx_max = find_delimiters(temp_ts.__dates__, f_day, l_day)

        res.append(
            temp_ts[idx_min:idx_max]
        )

        temp_ts = temp_ts[idx_max:]
        f_day += granularity.delta

    return res


def aggregate_on_first_day(
        ts: TimeSeries,
        granularity: Granularity = DailyGranularity(),
        method=sum,
        first_day_of_batch: int = 1,
        n_elements: int = -1
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity. Then aggregates each sub-set data into a single 
    TimeSeriesData to generate a new TimeSeries output.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to DailyGranularity().
        method (optional): Aggregation function. Defaults to sum.
        first_day_of_batch (int, optional): The day of the time step to use as 
        first delimiter. Defaults to 1.
        n_elements (int, optional): The length of the sub-set of the time step 
        to use. Defaults to 0.

    Returns:
        TimeSeries: A new time series with aggregated values.
    """
    assert n_elements > 0 or n_elements == - \
        1, "'n_elements' must be greater than 0 or set to -1 to get all elements."
    assert first_day_of_batch >= 1, "'first_day_of_batch' can't be lesser than 1."

    res = []

    fst_av_beg = granularity.get_first_available_beginning(day=ts.start_date)
    f_day = granularity.get_n_day_of_granularity(
        fst_av_beg, first_day_of_batch)

    temp_ts = ts.__deepcopy__()

    while f_day <= ts.end_date:
        if n_elements > 0:
            l_day = granularity.get_n_day_of_granularity(
                day=f_day, n=n_elements)
        else:
            l_day = granularity.get_end_of_granularity(day=f_day)

        idx_min, idx_max = find_delimiters(temp_ts.__dates__, f_day, l_day)

        aggregate_series = aggregate_dicts(
            [element.series for element in temp_ts[idx_min:idx_max]], method=method)

        res.append(
            TimeSeriesData(
                day=f_day,
                series=aggregate_series
            )
        )

        temp_ts = temp_ts[idx_max:]
        f_day += granularity.delta

    return TimeSeries(res)


def first_days(
        ts: TimeSeries,
        granularity: Granularity = DailyGranularity(),
        first_day_of_batch: int = 1
) -> TimeSeries:
    """
    Divides the input time series in many sub-sets for each contained time step 
    of the given granularity. Then returns a new TimeSeries with only the first 
    day of each batch.

    Args:
        ts (TimeSeries): Input time series.
        granularity (Granularity, optional): Time step to use to divide the 
        input series. Defaults to DailyGranularity().
        first_day_of_batch (int, optional): The day of the time step to use as 
        first delimiter. Defaults to 1.

    Returns:
        TimeSeries: A new time series with only a day for each step.
    """
    assert first_day_of_batch >= 1, "'first_day_of_batch' can't be lesser than 1."

    res = []
    fst_av_beg = granularity.get_first_available_beginning(day=ts.start_date)
    f_day = granularity.get_n_day_of_granularity(
        fst_av_beg, first_day_of_batch)

    while f_day <= ts.end_date:
        res.append(
            ts.get(day=f_day, else_empty=True)
        )

        f_day += granularity.delta

    return TimeSeries(res)
