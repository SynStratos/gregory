from datetime import datetime, date

import numpy as np
from outatime.granularity.granularity import MonthlyGranularity

from gregory.timeseries.time_series import TimeSeries
from test.utils import data_generation


def test_filter_by_title():
    ts = data_generation(start_date='2020-01-01', end_date='2020-01-10')
    res = ts.filter_by_title('pippo')
    assert set(res.titles) == {'pippo'}

    try:
        _ = ts.filter_by_title('paperino')
        raise AssertionError("Assertion error was not caught.")
    except AssertionError:
        pass


def test_as_array():
    ts = data_generation(start_date='2020-01-01', end_date='2020-01-05')
    ts_as_array = ts.as_array

    assert isinstance(ts_as_array, list), "Unexpected type."
    assert ts_as_array[0] == [datetime.strptime("2020-01-01", "%Y-%m-%d").date(), ts[0].data['pippo'], 'pippo']
    assert ts_as_array[1] == [datetime.strptime("2020-01-01", "%Y-%m-%d").date(), ts[0].data['pluto'], 'pluto']


def test_as_np_array():
    ts = data_generation(start_date='2020-01-01', end_date='2020-01-05')
    ts_as_np_array = ts.as_np_array()

    assert isinstance(ts_as_np_array, np.ndarray), "Unexpected type."


def test_interpolate():
    ts = data_generation(start_date='2020-01-01', end_date='2020-01-05')
    ts_int = ts.interpolate(title='pippo')
    assert ts_int[1].data != {}, "Missing data has not be filled."
    assert ts_int[1].data.get('pippo'), "Missing interpolated key."


def test_resample_inplace():
    def method(list_):
        if list_:
            return list_[0]
        else:
            return {}
    ts = data_generation(start_date='2020-01-01', end_date='2021-01-05')
    dates_a = ts.dates[:]
    as_array_a = ts.as_array
    ts.resample(granularity=MonthlyGranularity(), inplace=True, method=method)
    dates_b = ts.dates[:]
    as_array_b = ts.as_array
    assert dates_a != dates_b, "TimeSeries dates not refreshed after resample."
    assert as_array_a != as_array_b, "TimeSeries as_array not refreshed after resample."


def test_empty_time_series():
    try:
        _ = TimeSeries()
    except:
        raise AssertionError("Unable to create an empty time series.")


def test_update_from_array():
    ts = data_generation(start_date='2020-01-01', end_date='2020-01-05')
    ts_as_array = ts.as_array

    array_to_insert = [
        [date(2020, 1, 1), 999, 'topolino'],
        [date(2020, 1, 3), 998, 'topolino'],
    ]

    ts.update_from_array(array_to_insert)

    assert ts_as_array != ts.as_array, "Time series 'as_array' property did not change."

    assert 'topolino' in ts.get(date(2020, 1, 1)).data.keys(), "Missing 'topolino' in '2020-01-01' data."
    assert 'topolino' in ts.get(date(2020, 1, 3)).data.keys(), "Missing 'topolino' in '2020-01-03' data."
    assert 'topolino' == ts.as_array[2][2], "Missing 'topolino' in '2020-01-03' as array data."
    assert 'topolino' == ts.as_array[5][2], "Missing 'topolino' in '2020-01-03' as array data."

