from typing import List

from gregory.granularity.granularity import *
from gregory.timeseries.batches import batches
from gregory.timeseries.time_series import TimeSeries


def infer_ts_granularity(
        ts: TimeSeries,
        granularities: List = [YearlyGranularity, QuarterlyGranularity, MonthlyGranularity, WeeklyGranularity, DailyGranularity]
):
    output_delta = None
    output_granularity: Granularity
    ts.data_granularity = DailyGranularity()

    for granularity in granularities:
        g = granularity()
        _batches = batches(ts, g)

        lens = [len(batch) for batch in _batches]
        if max(lens) == 1:
            if output_delta:
                if output_delta < g.delta:
                    output_granularity = g
            else:
                output_delta = g.delta
                output_granularity = g

    if output_granularity:
        return output_granularity
    else:
        raise Exception("Unexpected granularity found in time series data.")
