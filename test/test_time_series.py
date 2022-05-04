from datetime import datetime

import numpy as np

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
