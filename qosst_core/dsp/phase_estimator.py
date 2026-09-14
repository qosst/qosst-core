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
Generic phase estimator.
"""

import abc
from typing import Optional

import numpy as np


# pylint: disable=too-few-public-methods
class BasePhaseEstimator(abc.ABC):
    """
    Abstract class for the phase estimator.
    """

    pilot_phase_filtering_size: int  #: Value for the uniform filter size of the phase.
    pilot_frequency_filtering_size: (
        int  #: Value for the uniform filter size of the frequency.
    )
    adc_rate: float  #: ADC rate in Sample/s.
    linewidth: float  #: Linewidth in Hz.

    def __init__(
        self,
        pilot_phase_filtering_size: int,
        pilot_frequency_filtering_size: int,
        adc_rate: float,
        linewidth: float,
    ) -> None:
        """
        Args:
            pilot_phase_filtering_size (int): Value for the uniform filter size of the phase.
            pilot_frequency_filtering_size (int): Value for the uniform filter size of the frequency.
            adc_rate (float): ADC rate in Sample/s.
            linewidth (float): Linewidth in Hz.
        """
        self.pilot_frequency_filtering_size = pilot_frequency_filtering_size
        self.pilot_phase_filtering_size = pilot_phase_filtering_size
        self.adc_rate = adc_rate
        self.linewidth = linewidth

    @abc.abstractmethod
    def estimate_phase(
        self, pilot_data: np.ndarray, shot_noise_data: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Estimate the phase.

        Args:
            pilot_data (np.ndarray): Data of the pilots.
            shot_noise_data (np.ndarray, optional): Data of the shot noise, may be used by some phase estimators. Defaults to None.

        Returns:
            np.ndarray: the estimated phase.
        """


class NoneBaseEstimator(BasePhaseEstimator):
    """
    NoneBaseEstimator.

    Raise a non implemented error.
    """

    def estimate_phase(
        self, pilot_data: np.ndarray, shot_noise_data: Optional[np.ndarray] = None
    ):
        raise NotImplementedError("NoneBaseEstimator should not be used in the DSP.")
