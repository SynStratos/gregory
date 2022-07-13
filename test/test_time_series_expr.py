from datetime import date, datetime

from test.utils import data_generation

from gregory.timeseries.expr import *
from gregory.timeseries.time_series import TimeSeries


def test_get_list_of_dates():
    ts_1 = data_generation(start_date='2020-01-01', end_date='2020-01-05')
    ts_2 = data_generation(start_date='2020-01-03', end_date='2020-01-07')
    res = get_list_of_dates([ts_1, ts_2])
    assert isinstance(res, list), "Unexpected type of result."
    assert all([isinstance(x, date) for y in res for x in y]), "Unexpected type of result elements."


def test_intersection_dates():
    dates_1 = [
        datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-02", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-04", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
    ]
    dates_2 = [
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-04", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-06", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-07", "%Y-%m-%d").date(),
    ]
    res = intersection_dates([dates_1, dates_2])
    assert isinstance(res, list), "Unexpected type of result."
    assert all([isinstance(x, date) for x in res]), "Unexpected type of result elements."

    expected_result = [
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-04", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
    ]

    assert res == expected_result, "Unexpected result content."


def test_union_dates():
    dates_1 = [
        datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-02", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-04", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
    ]
    dates_2 = [
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-04", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-06", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-07", "%Y-%m-%d").date(),
    ]
    res = union_dates([dates_1, dates_2])
    assert isinstance(res, list), "Unexpected type of result."
    assert all([isinstance(x, date) for x in res]), "Unexpected type of result elements."

    expected_result = [
        datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-02", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-04", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-06", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-07", "%Y-%m-%d").date(),
    ]

    assert res == expected_result, "Unexpected result content."


def take_first_available(a, b):
    if a is not None:
        return a
    elif b is not None:
        return b
    else:
        raise Exception("Both arguments are None.")


def test_union_type():
    ts_1 = data_generation(start_date='2020-01-01', end_date='2020-01-05')
    ts_2 = data_generation(start_date='2020-01-03', end_date='2020-01-07')
    res = union(ts_1, ts_2, conflict_method=take_first_available)
    assert isinstance(res, TimeSeries), "Unexpected type of result."


def test_intersection_type():
    ts_1 = data_generation(start_date='2020-01-01', end_date='2020-01-05')
    ts_2 = data_generation(start_date='2020-01-03', end_date='2020-01-07')
    res = intersection(ts_1, ts_2, conflict_method=take_first_available)
    assert isinstance(res, TimeSeries), "Unexpected type of result."


def first_or_empty(list_: list):
    list_ = [_el for _el in list_ if _el]
    try:
        return list_[0]
    except IndexError:
        return {}


def test_list_intersection():
    ts_1 = data_generation(start_date='2020-01-01', end_date='2020-01-06')
    ts_2 = data_generation(start_date='2020-01-03', end_date='2020-01-08')
    ts_3 = data_generation(start_date='2020-01-05', end_date='2020-01-09')

    res = list_intersection([ts_1, ts_2, ts_3], conflict_method=first_or_empty)
    assert isinstance(res, TimeSeries), "Unexpected type of result."
    expected_result_dates = [
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-06", "%Y-%m-%d").date(),
    ]
    assert expected_result_dates == res.dates, "Unexpected result content."


def test_list_union():
    ts_1 = data_generation(start_date='2020-01-01', end_date='2020-01-06')
    ts_2 = data_generation(start_date='2020-01-03', end_date='2020-01-08')
    ts_3 = data_generation(start_date='2020-01-05', end_date='2020-01-09')

    res = list_union([ts_1, ts_2, ts_3], conflict_method=first_or_empty)
    assert isinstance(res, TimeSeries), "Unexpected type of result."
    expected_result_dates = [
        datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-02", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-04", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-05", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-06", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-07", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-08", "%Y-%m-%d").date(),
        datetime.strptime("2020-01-09", "%Y-%m-%d").date(),
    ]
    assert expected_result_dates == res.dates, "Unexpected result content."