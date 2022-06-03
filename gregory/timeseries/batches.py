from typing import List

from outatime.granularity.granularity import Granularity, WeeklyGranularity
from outatime.timeseries.batches import aggregate as aggregate_
from outatime.timeseries.batches import split as split_
from outatime.timeseries.batches import pick_a_day as pick_a_day_
from outatime.timeseries.batches import pick_a_weekday as pick_a_weekday_

from ..timeseries.time_series import TimeSeries
from ..util.decorators import as_gregory_ts
from ..util.dictionaries import aggregate_dicts


def default_aggregation(x):
    return aggregate_dicts(x, method=sum)


@as_gregory_ts
def aggregate(
        ts: TimeSeries,
        method=default_aggregation,
        granularity: Granularity = WeeklyGranularity(),
        first_day_of_batch: int = 0,
        last_day_of_batch: int = -1,
        drop_tails: bool = False,
        store_day_of_batch: int = 0,
) -> TimeSeries:
    return aggregate_(ts, method, granularity, first_day_of_batch, last_day_of_batch, drop_tails, store_day_of_batch)


@as_gregory_ts
def pick_a_day(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        day_of_batch: int = -1,
        default=None,
) -> TimeSeries:
    if default is None:
        default = {}
    return pick_a_day_(ts, granularity, day_of_batch, default=default)


@as_gregory_ts
def pick_a_weekday(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        day_of_batch: int = -1,
        weekday: int = 1,
        default=None,
) -> TimeSeries:
    if default is None:
        default = {}
    return pick_a_weekday_(ts, granularity, day_of_batch, weekday, default=default)


@as_gregory_ts
def split(
        ts: TimeSeries,
        granularity: Granularity = WeeklyGranularity(),
        first_day_of_batch: int = 0,
        last_day_of_batch: int = -1,
        drop_tails: bool = False
) -> List[TimeSeries]:
    return split_(ts, granularity, first_day_of_batch, last_day_of_batch, drop_tails)
