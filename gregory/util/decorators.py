from outatime.util.decorators import *
from outatime.timeseries.time_series import TimeSeries as TimeSeries_
from gregory.timeseries.time_series import TimeSeries


def as_gregory_ts(func):
    """
    Decorator that transform an outatime TimeSeries output in a
    gregory TimeSeries.
    """
    def _wrap_outatime_func(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, TimeSeries_):
            return TimeSeries(res[:])
        elif isinstance(res, list) and isinstance(res[0], TimeSeries_):
            return [TimeSeries(x[:]) for x in res]
        else:
            raise TypeError("Wrapped function's output must be a outatime.timeseries.time_series.TimeSeries object (or list).")
    return _wrap_outatime_func

