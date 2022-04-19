# Gregory
Python Framework to Manage Time Series.

## Overview
The main goal of this framework is to simplify the collection of temporal data and related operations.
It is based on the concepts of **TimeSeries**, as a collection of records associated with a given day, and **Granularity**, to indicate a given time interval (e.g. daily, weekly, monthly, etc.).

The object related to a single day (**TimeSeriesData**) contains two attributes:
* day - the reference date for that record
* series - a dictionary that collects for each information (key) the relative value for that day

On the time series it is possible to carry out numerous operations of different types, as for example:
* add or remove records
* search records by date
* exclude records outside a determined range
* resampling of data
* interpolation of missing data
* union and intersection
* batch splitting and data aggregation
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
│   └── granularity_factory.py --> Factory class for creating granularity objects.
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