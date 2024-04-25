# qosst-core - Core module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2024 Yoann Piétri

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Digital Filters for CV-QKD.
"""
import abc
from typing import Tuple

import numpy as np
from scipy.signal import fftconvolve


def raised_cosine_filter(
    length: int, roll_off: float, symbol_period: float, sampling_rate: float
) -> Tuple[np.ndarray, np.ndarray]:
    """This function computes a raised cosine filter given the relevant parameters and returns the times and time response.

    Args:
        length (int): the length of the filter.
        roll_off (float): the roll-off factor. It must be between 0 and 1.
        symbol_period (float): the symbol period, in seconds.
        sampling_rate (float): the sampling rate in samples/second.

    Raises:
        ValueError: When the roll-off factor is not between 0 and 1.

    Returns:
        Tuple[np.ndarray, np.ndarray]: returns a tuple (times, h_rc) where times is the time array and h_rc the temporal response of the filter.
    """
    if roll_off < 0 or roll_off > 1:
        raise ValueError(
            f"The roll-off factor should be a number comprised between 0 and 1 (roll-off = {roll_off})."
        )
    eps = np.finfo(float).eps
    time_delta = 1 / float(sampling_rate)
    time_idx = ((np.arange(length) - length / 2)) * time_delta
    h_rc = np.zeros(length, dtype=float)
    denom = 1 - (
        ((2 * roll_off * time_idx) / symbol_period)
        * ((2 * roll_off * time_idx) / symbol_period)
    )
    idx1 = np.nonzero(
        np.bitwise_and(np.abs(denom) > np.sqrt(eps), np.abs(time_idx) > eps)
    )

    h_rc[idx1] = (
        np.sin(np.pi * time_idx[idx1] / symbol_period)
        / (np.pi * time_idx[idx1] / symbol_period)
    ) * (np.cos(np.pi * roll_off * time_idx[idx1] / symbol_period) / denom[idx1])

    idx2 = np.nonzero(
        np.bitwise_and(np.abs(denom) <= np.sqrt(eps), np.abs(time_idx) > eps)
    )

    h_rc[idx2] = (np.pi / 4) * (
        np.sin(np.pi * time_idx[idx2] / symbol_period)
        / (np.pi * time_idx[idx2] / symbol_period)
    )

    h_rc[np.abs(time_idx) < eps] = 1

    return time_idx, h_rc


def root_raised_cosine_filter(
    length: int, roll_off: float, symbol_period: float, sampling_rate: float
) -> Tuple[np.ndarray, np.ndarray]:
    """This function computes a root raised cosine filter given the relevant parameters and returns the times and time response.

    Args:
        length (int): the length of the filter.
        roll_off (float): the roll-off factor. It must be between 0 and 1.
        symbol_period (float): the symbol period, in seconds.
        sampling_rate (float): the sampling rate in samples/second.

    Raises:
        ValueError: When the roll-off factor is not between 0 and 1.

    Returns:
        Tuple[np.ndarray, np.ndarray]: returns a tuple (times, h_rc) where times is the time array and h_rc the temporal response of the filter.
    """
    if roll_off < 0 or roll_off > 1:
        raise ValueError(
            f"The roll-off factor should be a number comprised between 0 and 1 (roll-off = {roll_off})."
        )
    eps = np.finfo(float).eps
    time_delta = 1 / float(sampling_rate)
    time_idx = ((np.arange(length) - length / 2)) * time_delta
    h_rrc = np.zeros(length, dtype=float)

    denom = (
        np.pi
        * time_idx
        * (
            1
            - (4 * roll_off * time_idx / symbol_period)
            * (4 * roll_off * time_idx / symbol_period)
        )
        / symbol_period
    )
    idx1 = np.nonzero(
        np.bitwise_and(np.abs(denom) > np.sqrt(eps), np.abs(time_idx) > eps)
    )

    h_rrc[idx1] = (
        np.sin(np.pi * time_idx[idx1] * (1 - roll_off) / symbol_period)
        + 4
        * roll_off
        * (time_idx[idx1] / symbol_period)
        * np.cos(np.pi * time_idx[idx1] * (1 + roll_off) / symbol_period)
    ) / denom[idx1]

    idx2 = np.nonzero(
        np.bitwise_and(np.abs(denom) <= np.sqrt(eps), np.abs(time_idx) > eps)
    )

    if roll_off != 0:
        h_rrc[idx2] = (roll_off / np.sqrt(2)) * (
            ((1 + 2 / np.pi) * (np.sin(np.pi / (4 * roll_off))))
            + ((1 - 2 / np.pi) * (np.cos(np.pi / (4 * roll_off))))
        )
    else:
        h_rrc[idx2] = 0

    h_rrc[np.abs(time_idx) < eps] = 1.0 - roll_off + (4 * roll_off / np.pi)

    return time_idx, h_rrc


def rect_filter(length: int, symbol_period: float, sampling_rate: float):
    """Generates a rectangular filter.

    Args:
        length (int): length of filter.
        symbol_period (float): symbol period in seconds,
        sampling_rate (float): sampling rate in samples per second.

    Returns:
        Tuple[np.ndarray, np.ndarray]: returns a tuple (time, h) with time being the time array and h the coefficients of the filter.
    """
    coeffs = np.ones(length)
    time_delta = 1 / float(sampling_rate)
    time_idx = ((np.arange(length) - length / 2)) * time_delta

    coeffs[time_idx < -symbol_period / 2] = 0
    coeffs[time_idx > symbol_period / 2] = 0

    return time_idx, coeffs


class Filter(abc.ABC):
    """
    Generic filter.

    A filter has a times and filter attributes that are initialized by the
    __init__ and set_filter abstract methods.

    There is a also a mehtod apply filter to directly apply the current filter.
    """

    times: np.ndarray  #: time array.
    filter: np.ndarray  #: temporal response of the filter.

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the filter.
        """

    @abc.abstractmethod
    def set_filter(self, *args, **kwargs) -> None:
        """
        Generate the filter.
        """

    def get_filter(self) -> np.ndarray:
        """Returns the temporal response of the filter.

        Returns:
            np.ndarray: the temporal response of the filter.
        """
        return self.filter

    def get_times(self) -> np.ndarray:
        """Returns the time array.

        Returns:
            np.ndarray: the time array.
        """
        return self.times

    def apply_filter(self, data: np.ndarray) -> np.ndarray:
        """Apply the filter to data and returns the filtered data.

        This methods uses the fftconvolve from scipy to apply the filter.

        Args:
            data (np.ndarray): data that needs to be filtered.

        Raises:
            ValueError: if the filter has not been set.

        Returns:
            np.ndarray: the filtered data.
        """
        if not self.filter:
            raise ValueError("Cannot apply filter if it's not set.")
        return fftconvolve(data, self.filter, mode="same")


class RaisedCosineFilter(Filter):
    """
    Filter class for a Raised cosine filter.
    """

    length: int  #: The length of the filter.
    roll_off: float  #: The roll-off factor of the filter.
    symbol_period: float  #: The symbol period of the filter, in seconds.
    sampling_rate: float  #: The sampling rate, in samples/second.

    bandwidth: float  #: The computed bandwidth of the filter.

    def __init__(
        self,
        length: int,
        roll_off: float,
        symbol_period: float,
        sampling_rate: float,
        *args,
        **kwargs,
    ) -> None:
        """
        Args:
            length (int): length of the filter.
            roll_off (float): roll-off factor of the filter, between 0 and 1.
            symbol_period (float): symbol period, in seconds.
            sampling_rate (float): sampling rate, in samples/second.

        Raises:
            ValueError: if the roll-off factor is not between 0 and 1.
        """
        self.length = length
        if roll_off < 0 or roll_off > 1:
            raise ValueError(
                f"The roll-off factor should be a number comprised between 0 and 1 (roll-off = {roll_off})."
            )
        self.roll_off = roll_off
        self.symbol_period = symbol_period
        self.sampling_rate = sampling_rate

        self.bandwidth = (1 + roll_off) / symbol_period

        self.set_filter()

    def set_filter(self, *args, **kwargs) -> None:
        """
        Set the filter using the :func:`~cvqkd_core.comm.filters.raised_cosine_filter` function.
        """
        self.times, self.filter = raised_cosine_filter(
            self.length, self.roll_off, self.symbol_period, self.sampling_rate
        )


class RootRaisedCosineFilter(Filter):
    """
    Filter class with a Root Raised cosine filter.
    """

    length: int  #: The length of the filter.
    roll_off: float  #: The roll-off factor of the filter.
    symbol_period: float  #: The symbol period of the filter, in seconds.
    sampling_rate: float  #: The sampling rate, in samples/second.

    bandwidth: float  #: The computed bandwidth of the filter.

    def __init__(
        self,
        length: int,
        roll_off: float,
        symbol_period: float,
        sampling_rate: float,
        *args,
        **kwargs,
    ) -> None:
        """
        Args:
            length (int): length of the filter.
            roll_off (float): roll-off factor of the filter, between 0 and 1.
            symbol_period (float): symbol period, in seconds.
            sampling_rate (float): sampling rate, in samples/second.

        Raises:
            ValueError: if the roll-off factor is not between 0 and 1.
        """
        self.length = length
        if roll_off < 0 or roll_off > 1:
            raise ValueError(
                f"The roll-off factor should be a number comprised between 0 and 1 (roll-off = {roll_off})."
            )

        self.roll_off = roll_off
        self.symbol_period = symbol_period
        self.sampling_rate = sampling_rate

        self.bandwidth = (1 + roll_off) / symbol_period

        self.set_filter()

    def set_filter(self, *args, **kwargs) -> None:
        """
        Set the filter using the :func:`~cvqkd_core.comm.filters.root_raised_cosine_filter` function.
        """
        self.times, self.filter = root_raised_cosine_filter(
            self.length, self.roll_off, self.symbol_period, self.sampling_rate
        )


class RectFilter(Filter):
    """
    Filter class with a Rectangular filter.
    """

    length: int  #: The length of the filter.
    symbol_period: float  #: The symbol period of the filter, in seconds.
    sampling_rate: float  #: The sampling rate, in samples/second.

    def __init__(
        self,
        length: int,
        symbol_period: float,
        sampling_rate: float,
        *args,
        **kwargs,
    ) -> None:
        """
        Initialization function
        """
        self.length = length
        self.symbol_period = symbol_period
        self.sampling_rate = sampling_rate

        self.set_filter()

    def set_filter(self, *args, **kwargs) -> None:
        """
        Set the filter using the :func:`~cvqkd_core.comm.filters.rect_filter` function.
        """
        self.times, self.filter = rect_filter(
            self.length, self.symbol_period, self.sampling_rate
        )
