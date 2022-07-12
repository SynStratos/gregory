from math import ceil, floor
import numpy as np
from typing import Tuple

from statsmodels.tsa.seasonal import seasonal_decompose

from ..granularity.granularity import Granularity
from ..timeseries.time_series import TimeSeries


def moving_average(series: np.ndarray, window_size: int, mode: str = 'same') -> np.ndarray:
    """
    Method to apply the moving average smoothing to the give time series.

    Args:
        series (np.ndarray): Input data.
        window_size (int): Size of the window used for the moving average.
        mode (str): Defines the convolution modality (defaults to 'same').

    Returns:
        np.ndarray: Smoothed output data.
    """

    # create denominator to manage starting and ending part of the timeseries
    denominator = np.full((1, len(series)), window_size, dtype=int)
    head_window_size = ceil((window_size - 1)/2)
    tail_window_size = floor((window_size - 1)/2)

    if tail_window_size > 0:
        window_head = np.arange(-head_window_size, 0)
        window_tail = np.flip(np.arange(-tail_window_size, 0))
        denominator[:, :head_window_size] += window_head
        denominator[:, -tail_window_size:] += window_tail

    return np.divide(np.convolve(a=series, v=np.ones(window_size), mode=mode), denominator)


def trend_and_seasonality(series: np.ndarray, freq: int, window_size: int) -> Tuple:
    """
    Extracts trend and seasonal components from time series.

    Args:
        series (np.ndarray): Input data.
        freq (int): Number of occurrences per year.
        window_size (int): Size of the window used for the moving average.

    Returns:
        Tuple: Array with trend data, array with seasonality data.
    """
    window_size = min([window_size, ceil(len(series) / 4)])

    result = seasonal_decompose(
        series,
        model='additive',
        period=freq,
        extrapolate_trend='freq'
    )

    trend = moving_average(series=result.trend, window_size=window_size)
    seasonality = result.seasonal
    return trend, seasonality


def add_trend_seasonality(
        ts: TimeSeries,
        granularity: Granularity = None,
        window_size: int = 12,
        label: str = None,
        trend_label: str = "trend",
        seasonality_label: str = "seasonality"
) -> TimeSeries:
    """
    Adds trend and seasonality data to the given timeseries.

    Args:
        ts (TimeSeries): Input timeseries data.
        granularity (Granularity, optional): Get the time delta used for frequency. Defaults to None.
        window_size (int): Size of the window used for the moving average.
        label (str, optional): Select only a label to calculate trend and seasonality on its data.
        Defaults to None.
        trend_label (str, optional): Specify the label of the trend data. Defaults to "trend".
        seasonality_label (str, optional):  Specify the label of the seasonality data.
        Defaults to "seasonality".

    Returns:
        TimeSeries: Output timeseries with trend and seasonality information.
    """
    source = ts.as_np_array()
    if label:
        where = source[:, 2] == label
        source = source[where]
    series = source[:, 1]

    delta = granularity.delta if granularity else ts.data_granularity.delta
    frequency = 1 // delta.total_years

    trend, seasonality = trend_and_seasonality(
        series,
        freq=int(frequency),
        window_size=window_size
    )

    trend_all = source.copy()
    trend_all[:, 1] = np.round(trend, 2)
    trend_all[:, 2] = trend_label

    seasonality_all = source.copy()
    seasonality_all[:, 1] = np.round(seasonality, 2)
    seasonality_all[:, 2] = seasonality_label

    if frequency == 1:
        series = trend_all
    else:
        series = np.concatenate((trend_all, seasonality_all), axis=0)

    mask = np.isnan(series[:, 1].astype(float))
    series = series[~mask]

    resulting_list = ts.copy()
    resulting_list.update_from_array(
        series
    )
    return resulting_list
