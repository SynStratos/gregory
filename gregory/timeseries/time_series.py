from copy import copy
from datetime import date
from functools import cached_property
from typing import List
import numpy as np
from scipy.interpolate import interp1d

from ..dataclass.time_series_data import TimeSeriesData
from ..granularity.granularity import Granularity, DailyGranularity
from ..util.agenda import calendar_by_steps
from ..util.bisect import index_of, find_delimiters


def get_day(x):
    return x.day


class TimeSeries(List[TimeSeriesData]):
    """
    Class that inherits list to add useful methods for time series management.
    It contains only TimeSeriesData objects as elements.
    """
    def __clear_cache__(self):
        """Clear all cached properties."""
        if hasattr(self, 'as_array'):
            del self.as_array
        if hasattr(self, '__indexes__'):
            del self.__indexes__
        if hasattr(self, 'titles'):
            del self.titles
        if hasattr(self, '__dates__'):
            del self.__dates__

    def __refresh__(self):
        """Sort the timeseries by date and reset its properties."""
        self.__sort__()
        self.__clear_cache__()

    def __sort__(self):
        """Sort the timeseries by date."""
        self.sort(key=get_day)

    def __init__(self, data=[]):
        super().__init__(data)
        self.__sort__()

    def __setitem__(self, key, value):
        super(TimeSeries, self).__setitem__(key, value)
        self.__refresh__()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__class__(super(TimeSeries, self).__getitem__(item))
        else:
            return super(TimeSeries, self).__getitem__(item)

    def __add__(self, other):
        super().__add__(other)
        self.__refresh__()

    def __delitem__(self, idx):
        super().__delitem__(idx)
        self.__refresh__()

    def __deepcopy__(self):
        return self.__class__([copy(element) for element in self])

    @property
    def start_date(self) -> date:
        return self[0].day

    @property
    def end_date(self) -> date:
        return self[-1].day

    @cached_property
    def as_array(self):
        """
        Return the time series as an array, with a row for each series value.

        Example:
            [TimeSeriesData(day=2022-04-16, series={'a': 1, 'b': 8})]

            returns [[2022-04-16, 1, 'a'], [2022-04-16, 8, 'b']]
        """
        return [[el.day, v, k] for el in self for k, v in el.series.items()]

    @cached_property
    def __dates__(self):
        """List of all dates available in the time series."""
        return [data.day for data in self]

    @cached_property
    def __indexes__(self):
        """Maps dates to their indexes in the time series."""
        return {day.strftime("%Y-%m-%d"): idx for idx, day in enumerate(self.__dates__)}

    @cached_property
    def titles(self):
        """List of possible TITLES in the time series data."""
        return sorted(set([k for item in self for k in item.series.keys()]))

    def append(self, __object: TimeSeriesData):
        """Add a new TimeSeriesData object to the time series."""
        assert isinstance(__object, TimeSeriesData), "Only TimeSeriesData objects can be appended."
        super(TimeSeries, self).append(__object)
        self.__refresh__()

    def copy(self):
        return self.__deepcopy__()

    def delete(self, day: date):
        idx = index_of(self.__dates__, day)
        self.__delitem__(idx)

    def update(self, __list: List[TimeSeriesData]):
        """
        Add all elements of the given list of TimeSeriesData to the time series.
        Updates existing elements if already in the time series.

        Args:
            __list (List[TimeSeriesData]): Input list of new elements.
        """
        for new_element in __list:
            try:
                stored_element = self.get(new_element.day)
                stored_element.series.update(new_element.series)
            except KeyError:
                self.append(new_element)

    def update_from_array(self, __array: list):
        """
        Add all data of the given array to the time series.
        Updates existing elements if already in the time series.
        Input array must be in the following format:
            [[date, value, title]]

        Args:
            __array (list): Input array of new data.
        """
        for new_element in __array:
            try:
                stored_element = self.get(new_element[0])
                stored_element.series.update(
                    {new_element[2]: new_element[1]}
                )
            except KeyError:
                self.append(
                    TimeSeriesData(
                        day=new_element[0],
                        series={new_element[2]: new_element[1]}
                    )
                )

    def get(self, day: date, else_empty: bool = False) -> TimeSeriesData:
        """
        Search the time series element for the given day.

        Args:
            day (date): The day to search in the time series.
            else_empty (bool, optional): If set to True, a TimeSeriesData with 
            empty 'series' is return when the value is not found. Defaults to 
            False.

        Raises:
            KeyError: An exception is returned when the day is not found.

        Returns:
            TimeSeriesData: A time series element for the searched day.
        """
        try:
            return self[index_of(self.__dates__, day)]
        except (KeyError, ValueError):
            if else_empty:
                return TimeSeriesData(day=day, series={})
            raise KeyError

    def get_series_or_empty(self, day: date):
        """
        Get the TimeSeriesData series for the given day or return an empty 
        dictionary if missing.
        """
        return self.get(day, else_empty=True).series

    def as_np_array(self) -> np.ndarray:
        """
        Return the time series as a numpy array, with a row for each series 
        value.
        """
        return np.array(self.as_array)

    def cut(self, min_date: date, max_date: date, inplace: bool = False):
        """
        Cut the time series selecting only the available days between the
        input delimiters.

        Args:
            min_date (date): Minimum date of range.
            max_date (date): Maximum date of range.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        idx_min, idx_max = find_delimiters(self.__dates__, min_date, max_date)

        if inplace:
            self[:] = self[idx_min:idx_max]
            self.__clear_cache__()
        else:
            return self.__deepcopy__()[idx_min:idx_max]

    def resample(self, granularity: Granularity = DailyGranularity(), inplace: bool = False):
        """
        Select only needed days for the given granularity.
        If a day is missing, create a new TimeSeriesData with empty series.

        Example:
            [TimeSeriesData(day=2022-04-14, series={'a': 1, 'b': 8}),
            TimeSeriesData(day=2022-04-16, series={'a': 3, 'b': 8})]

            granularity = DailyGranularity()

            Returns:
                [TimeSeriesData(day=2022-04-14, series={'a': 1, 'b': 8}),
                TimeSeriesData(day=2022-04-15, series={}),
                TimeSeriesData(day=2022-04-16, series={'a': 3, 'b': 8})]

        Args:
            granularity (Granularity, optional): Time step to use for
            selecting ranges. Defaults to DailyGranularity().
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        first_day = granularity.get_first_available_beginning(self.start_date)
        days = calendar_by_steps(
            start_date=first_day,
            end_date=self.end_date,
            step=granularity.delta
        )

        resampled = [self.__deepcopy__().get(day, else_empty=True) for day in days]

        if inplace:
            self[:] = resampled
        else:
            return TimeSeries(resampled)

    def interpolate(self, title: str, method: str = 'linear', inplace: bool = False):
        """
        Fill missing values for a given key of time series data.

        Example:
            [TimeSeriesData(day=2022-04-14, series={'a': 1, 'b': 8}),
            TimeSeriesData(day=2022-04-15, series={}),
            TimeSeriesData(day=2022-04-16, series={'a': 3, 'b': 8})]

            title = 'a'

            Returns:
                [TimeSeriesData(day=2022-04-14, series={'a': 1, 'b': 8}),
                TimeSeriesData(day=2022-04-15, series={'a': 2}),
                TimeSeriesData(day=2022-04-16, series={'a': 3, 'b': 8})]

        Args:
            title (str): The value to fill.
            method (str, optional): Interpolation method. Defaults to 'linear'.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        filtered = self.filter_by_title(title=title, inplace=False)
        filtered_array = [[el.day, el.series.get(
            title, None), title] for el in filtered]

        filtered_array_np = np.array(filtered_array)

        y = np.array(filtered_array_np[:, 1], dtype=np.float)
        x = np.arange(0, len(y))
        not_nan_y = y[~np.isnan(y)]
        not_nan_x = np.argwhere(~np.isnan(y)).reshape([-1])

        interpol_f = interp1d(x=not_nan_x, y=not_nan_y, kind=method)

        filtered_array_np[:, 1] = interpol_f(x)

        if inplace:
            self.update_from_array(filtered_array_np)
        else:
            temp_ts = self.__deepcopy__()
            temp_ts.update_from_array(filtered_array_np)
            return temp_ts

    def filter_by_title(self, title: str, inplace: bool = False):
        """
        Filter the time series to return only the given key for all days.

        Example:
            [TimeSeriesData(day=2022-04-14, series={'a': 1, 'b': 8}),
            TimeSeriesData(day=2022-04-15, series={'b': 7}),
            TimeSeriesData(day=2022-04-16, series={'a': 3, 'b': 8})]

            title = 'a'

            Returns:
                [TimeSeriesData(day=2022-04-14, series={'a': 1}),
                TimeSeriesData(day=2022-04-15, series={}),
                TimeSeriesData(day=2022-04-16, series={'a': 3})]

        Args:
            title (str): Given key.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        assert title in self.titles, "requested title is missing"

        temp_ts = self.__deepcopy__()
        for element in temp_ts:
            try:
                element.series = {title: element.series.get(title)}
            except KeyError:
                element.series = {}

        if inplace:
            self[:] = temp_ts
        else:
            return temp_ts

    def filter_by_value(self, value, inplace: bool = False):
        raise NotImplementedError
