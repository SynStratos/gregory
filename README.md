# Gregory
Python Framework to Manage Time Series structured as one-level dictionaries.

## Overview
This framework is an extension of the **[OUTATIME](https://github.com/SynStratos/outatime)** package to facilitate operations on time series built as dictionaries.

The main requirement is that the _data_ attribute of the dataclass **TimeSeriesData** is a one-level dictionary.

E.g.
```
TimeSeriesData(
    day=date('2022-04-28'),
    date={
        'gold': 1887.77,
        'silver': 23.03
    }
)
```

Some features are added such as:
* interpolation of missing data
* trend and seasonality calculation
* methods of aggregation between dictionaries
* other

## Installation
```
pip install gregory
```

## Framework Structure
```
gregory
│
├── timeseries
│   ├── batches.py --> Set of methods to operate on time series dividing them into batches.
│   ├── processing.py --> Set of methods to elaborate time series.
│   └── time_series.py --> Core class that represents a series of daily records.
│
└── util
    └── dictionaries.py --> Utils related to operations on dictionaries.
```

## License
MIT license, see ``LICENSE`` file.