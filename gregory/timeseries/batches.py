from outatime.granularity.granularity import Granularity, WeeklyGranularity
from outatime.timeseries.batches import aggregate as o_aggregate

from ..timeseries.time_series import TimeSeries
from ..util.dictionaries import aggregate_dicts


def default_aggregation(x):
    return aggregate_dicts(x, method=sum)


def aggregate(
        ts: TimeSeries,
        method=default_aggregation,
        granularity: Granularity = WeeklyGranularity(),
        first_day_of_batch: int = 0,
        last_day_of_batch: int = -1,
        drop_tails: bool = False,
        store_day_of_batch: int = 0,
) -> TimeSeries:
    return o_aggregate(ts, method, granularity, first_day_of_batch, last_day_of_batch, drop_tails, store_day_of_batch)
