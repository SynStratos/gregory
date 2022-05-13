# Gregory
Python Framework to Manage Time Series structured as one-level dictionaries.

## Overview
This framework is an extension of the **[OUTATIME](https://github.com/SynStratos/outatime)** package to facilitate operations on time series built as dictionaries.

The main requirement is that the _data_ attribute of the dataclass **TimeSeriesData** is a one-level dictionary.

E.g.
```
TimeSeriesData(
    day=date('2022-04-28'),
    data={
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
├── dataclass
│   └── time_series_data.py --> Class used to manage daily data.
│
├── granularity
│   ├── granularity.py --> Set of classes used for managing time intervals of different length.
│   ├── granularity_factory.py --> Factory class for creating granularity objects.
│   └── utils.py --> Utils related to granularities.
│
├── timeseries
│   ├── batches.py --> Set of methods to operate on time series dividing them into batches.
│   ├── expr.py --> Set of operations between time series.
│   ├── processing.py --> Set of methods to elaborate time series.
│   └── time_series.py --> Core class that represents a series of daily records.
│
└── util
    ├── agenda.py --> Utils related to calendar info and evalutations.
    ├── bisect.py --> Utils related to binary search.
    ├── decorators.py --> Useful decorators.
    ├── dictionaries.py --> Utils related to operations on dictionaries.
    └── relativedelta.py --> Class that extends relativedelta with useful properties.
```

## License
MIT license, see ``LICENSE`` file.