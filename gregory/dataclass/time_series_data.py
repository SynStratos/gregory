from dataclasses import dataclass
from typing import Dict
from datetime import date


@dataclass
class TimeSeriesData:
    day: date
    series: Dict
