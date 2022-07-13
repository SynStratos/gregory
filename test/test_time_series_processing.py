from gregory.timeseries.processing import add_trend_seasonality
from test.utils import data_generation


def test_add_trend_seasonality_default():
    ts = data_generation(start_date='2017-01-01', end_date='2020-12-31')
    res = add_trend_seasonality(ts=ts)
    assert "trend" in res.titles, "Missing 'trend' in resulting data"
    assert "seasonality" in res.titles, "Missing 'seasonality' in resulting data"


def test_add_trend_seasonality_single_label():
    ts = data_generation(start_date='2017-01-01', end_date='2020-12-31')
    res = add_trend_seasonality(
        ts=ts,
        label='pluto'
    )
    assert "pluto" in res.titles, "Missing 'pluto' in resulting data"
    assert "pippo" in res.titles, "Missing 'pippo' in resulting data"
    assert "trend" in res.titles, "Missing 'trend' in resulting data"
    assert "seasonality" in res.titles, "Missing 'seasonality' in resulting data"


def test_add_trend_seasonality_target_labels():
    ts = data_generation(start_date='2017-01-01', end_date='2020-12-31')
    res = add_trend_seasonality(
        ts=ts,
        trend_label='test_trend',
        seasonality_label='test_seasonality',
    )
    assert "trend" not in res.titles, "Unexpected 'trend' in resulting data"
    assert "seasonality" not in res.titles, "Unexpected 'seasonality' in resulting data"
    assert "test_trend" in res.titles, "Missing 'test_trend' in resulting data"
    assert "test_seasonality" in res.titles, "Missing 'test_seasonality' in resulting data"
