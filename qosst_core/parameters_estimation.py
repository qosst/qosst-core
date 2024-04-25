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
Definition of BaseEstimator for qosst_bob.

Definition of NoneEstimator for the configuration.
"""
import abc
from typing import Tuple

import numpy as np


# pylint: disable=too-few-public-methods
class BaseEstimator(abc.ABC):
    """
    Base estimator.
    """

    @staticmethod
    @abc.abstractmethod
    def estimate(
        alice_symbols: np.ndarray,
        bob_symbols: np.ndarray,
        alice_photon_number: float,
        electronic_symbols: np.ndarray,
        electronic_shot_symbols: np.ndarray,
    ) -> Tuple[float, float, float]:
        """
        Estimate the transmittance and excess noise given
        the symbols of Alice and Bob, symbols for the shot noise and
        electronic noise and the avarage photon number at Alice's output.

        Transmittance should be here understood as total transmittance hence
        eta * T.

        Args:
            alice_symbols (np.ndarray): symbols sent by Alice.
            bob_symbols (np.ndarray): symbols received by Bob, after DSP.
            alice_photon_number (float): average number of photon at Alice's output.
            electronic_symbols (np.ndarray): electronic noise data after equivalent DSP.
            electronic_shot_symbols (np.ndarray): electronic and shot noise data, after equivalent DSP.

        Returns:
            Tuple[float, float, float]: tuple containing the transmittance, the excess noise at Bob side and the electronic noise.
        """


class NoneEstimator(BaseEstimator):
    """
    Fake Estimator.

    Always return 0 for the estimation.
    """

    @staticmethod
    def estimate(
        _alice_symbols: np.ndarray,
        _bob_symbols: np.ndarray,
        _alice_photon_number: float,
        _electronic_symbols: np.ndarray,
        _electronic_shot_symbols: np.ndarray,
    ) -> Tuple[float, float, float]:
        """
        Estimate with a fake estimator, and always return 0.

        Args:
            _alice_symbols (np.ndarray): ignored.
            _bob_symbols (np.ndarray): ignored.
            _alice_photon_number (float): ignored.
            _electronic_symbols (np.ndarray): ignored.
            _electronic_shot_symbols (np.ndarray): ignored.

        Returns:
            Tuple[float, float, float]: 0, 0, 0.
        """
        return 0, 0, 0
