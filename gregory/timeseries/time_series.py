from copy import deepcopy
from datetime import date
from functools import cached_property
import numpy as np
from scipy.interpolate import interp1d

from outatime.timeseries.time_series import TimeSeries as TS
from outatime.dataclass.time_series_data import TimeSeriesData


class TimeSeries(TS):

    def __clear_cache(self):
        """Clear all cached properties."""
        super().__clear_cache()
        if hasattr(self, 'as_array'):
            del self.as_array
        if hasattr(self, 'titles'):
            del self.titles

    @cached_property
    def as_array(self):
        """
        Return the time series as an array, with a row for each series value.

        Example:
            [TimeSeriesData(day=2022-04-16, series={'a': 1, 'b': 8})]

            returns [[2022-04-16, 1, 'a'], [2022-04-16, 8, 'b']]
        """
        return [[el.day, v, k] for el in self for k, v in el.data.items()]

    @cached_property
    def titles(self):
        """List of possible TITLES in the time series data."""
        return sorted(set([k for item in self for k in item.data.keys()]))

    def keys(self):
        return {day.strftime("%Y-%m-%d") for day in self.dates}

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
                stored_element.data.update(
                    {new_element[2]: new_element[1]}
                )
            except KeyError:
                self.append(
                    TimeSeriesData(
                        day=new_element[0],
                        data={new_element[2]: new_element[1]}
                    )
                )

    def get_series_or_empty(self, day: date):
        """
        Get the TimeSeriesData data for the given day or return an empty
        dictionary if missing.
        """
        return self.get(day, value={}).data

    def as_np_array(self) -> np.ndarray:
        """
        Return the time series as a numpy array, with a row for each data
        value.
        """
        return np.array(self.as_array)

    def interpolate(self, title: str, method: str = 'linear', inplace: bool = False):
        """
        Fill missing values for a given key of time series data.

        Example:
            [TimeSeriesData(day=2022-04-14, data={'a': 1, 'b': 8}),
            TimeSeriesData(day=2022-04-15, data={}),
            TimeSeriesData(day=2022-04-16, data={'a': 3, 'b': 8})]

            title = 'a'

            Returns:
                [TimeSeriesData(day=2022-04-14, data={'a': 1, 'b': 8}),
                TimeSeriesData(day=2022-04-15, data={'a': 2}),
                TimeSeriesData(day=2022-04-16, data={'a': 3, 'b': 8})]

        Args:
            title (str): The value to fill.
            method (str, optional): Interpolation method. Defaults to 'linear'.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        filtered = self.filter_by_title(title=title, inplace=False)
        filtered_array = [[el.day, el.data.get(
            title, None), title] for el in filtered]

        filtered_array_np = np.array(filtered_array)

        y = np.array(filtered_array_np[:, 1], dtype=np.float64)
        x = np.arange(0, len(y))
        not_nan_y = y[~np.isnan(y)]
        not_nan_x = np.argwhere(~np.isnan(y)).reshape([-1])

        interpol_f = interp1d(x=not_nan_x, y=not_nan_y, kind=method)

        filtered_array_np[:, 1] = interpol_f(x)

        if inplace:
            self.update_from_array(filtered_array_np)
        else:
            temp_ts = deepcopy(self)
            temp_ts.update_from_array(filtered_array_np)
            return temp_ts

    def filter_by_title(self, title: str, inplace: bool = False):
        """
        Filter the time series to return only the given key for all days.

        Example:
            [TimeSeriesData(day=2022-04-14, data={'a': 1, 'b': 8}),
            TimeSeriesData(day=2022-04-15, data={'b': 7}),
            TimeSeriesData(day=2022-04-16, data={'a': 3, 'b': 8})]

            title = 'a'

            Returns:
                [TimeSeriesData(day=2022-04-14, data={'a': 1}),
                TimeSeriesData(day=2022-04-15, data={}),
                TimeSeriesData(day=2022-04-16, data={'a': 3})]

        Args:
            title (str): Given key.
            inplace (bool, optional): Original time series is overwritten
            if set to True. Defaults to False.
        """
        assert title in self.titles, "requested title is missing"

        temp_ts = deepcopy(self)
        for element in temp_ts:
            try:
                element.data = {title: element.data.get(title)}
            except KeyError:
                element.data = {}

        temp_ts.__clear_cache()

        if inplace:
            self[:] = temp_ts
        else:
            return temp_ts
