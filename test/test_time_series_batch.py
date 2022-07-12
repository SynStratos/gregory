from outatime.granularity.granularity import MonthlyGranularity

from gregory.timeseries.batches import aggregate, pick_a_day, pick_a_weekday, split
from gregory.timeseries.time_series import TimeSeries
from test.utils import data_generation


def take_first(_list):
    if _list:
        return _list[0]
    return None


def test_aggregate():
    tsl = data_generation()
    res = aggregate(tsl, granularity=MonthlyGranularity(), method=take_first)
    assert isinstance(res, TimeSeries), "Unexpected type of result."


def test_pick_a_day():
    tsl = data_generation()
    res = pick_a_day(tsl, granularity=MonthlyGranularity(), day_of_batch=0)
    assert isinstance(res, TimeSeries), "Unexpected type of result."


def test_pick_a_weekday():
    tsl = data_generation()

    res = pick_a_weekday(
        ts=tsl,
        granularity=MonthlyGranularity(),
        day_of_batch=-1,
        weekday=0
    )
    assert isinstance(res, TimeSeries), "Unexpected type of result."


def test_split():
    tsl = data_generation()
    res = split(tsl, granularity=MonthlyGranularity())
    assert isinstance(res, list), "Unexpected type of result."
    assert all([isinstance(x, TimeSeries) for x in res]), "Unexpected type of result content."