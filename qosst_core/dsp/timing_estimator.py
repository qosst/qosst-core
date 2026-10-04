# qosst-core - Core module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2026 Yoann Piétri
# Copyright (C) 2021-2026 Thomas Liege

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
Generic timing recovery estimator.
"""

import abc
from typing import Optional

import numpy as np


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class BaseTimingRecoveryEstimator(abc.ABC):
    """
    Abstract class for the timing recovery estimator.
    """

    sps: float  #: Samples per symbol.
    adc_rate: float  #: ADC rate in Sample per second.
    num_symbols: int  #: Total number of symbols.
    subframe_length: int  #: Number of symbols in a subframe.
    symbol_timing_oversampling: int  #: Factor by which the signal is oversampled when searching for the optimal symbol sampling time.
    roll_off: float  #: Roll-off factor of the root raised cosine filter.
    symbol_rate: float  #: Symbol rate in Baud.
    pilots_frequencies: np.ndarray[float]  #: Array of frequencies for the pilots.
    frequency_shift: float  #: Frequency shift of the quantum data.
    num_samples_previous_subframe: (
        int  #: Number of samples recovered in the previous subframe.
    )
    pulsed_sampling: bool  #: Wether to use the pulse sampling method, which consists in convolving the signal with a rectangular pulse of width equal to the symbol period, and then sampling at the symbol rate.

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(
        self,
        sps: float,
        adc_rate: float,
        num_symbols: int,
        subframe_length: int,
        symbol_timing_oversampling: int,
        roll_off: float,
        symbol_rate: float,
        pilots_frequencies: np.ndarray,
        frequency_shift: float,
        num_samples_previous_subframe: int,
        pulsed_sampling: bool = False,
    ) -> None:
        """
        Args:
            sps (float): Samples per symbol.
            adc_rate (float): _desADC rate in Sample per second.cription_
            num_symbols (int):  Total number of symbols.
            subframe_length (int): Number of symbols in a subframe.
            symbol_timing_oversampling (int): actor by which the signal is oversampled when searching for the optimal symbol sampling time.
            roll_off (float): Roll-off factor of the root raised cosine filter.
            symbol_rate (float): Symbol rate in Baud.
            pilots_frequencies (np.ndarray): Array of frequencies for the pilots.
            frequency_shift (float): Frequency shift of the quantum data.
            num_samples_previous_subframe (int): Number of samples recovered in the previous subframe.
            pulsed_sampling (bool, optional): Wether to use the pulse sampling method, which consists in convolving the signal with a rectangular pulse of width equal to the symbol period, and then sampling at the symbol rate. Defaults to False.
        """
        self.sps = sps
        self.adc_rate = adc_rate
        self.num_symbols = num_symbols
        self.subframe_length = subframe_length
        self.symbol_timing_oversampling = symbol_timing_oversampling
        self.roll_off = roll_off
        self.symbol_rate = symbol_rate
        self.pilots_frequencies = pilots_frequencies
        self.frequency_shift = frequency_shift
        self.num_samples_previous_subframe = num_samples_previous_subframe
        self.pulsed_sampling = pulsed_sampling

    @abc.abstractmethod
    def sample(
        self, data: np.ndarray, pilot_data: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Estimate the sampling points.

        Args:
            data (np.ndarray): data to sample
            pilot_data (Optional[np.ndarray]): Optional data to give that maybe be used by some sampling estimators. Default to None.

        Returns:
            np.ndarray: the estimated sampling points.
        """


class NoneTimingRecoveryEstimator(BaseTimingRecoveryEstimator):
    """
    NoneTimingRecoveryEstimator.

    Raise a non implemented error.
    """

    def sample(self, data: np.ndarray, pilot_data: Optional[np.ndarray] = None):
        raise NotImplementedError(
            "NoneTimingRecoveryEstimator should not be used in the DSP."
        )
