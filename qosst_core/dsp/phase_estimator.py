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

import numpy as np


# pylint: disable=too-few-public-methods
class BasePhaseEstimator(abc.ABC):
    """
    Abstract class for the phase estimator.
    """

    def __init__(self, **_kwargs) -> None:
        pass

    @abc.abstractmethod
    def estimate_phase(self) -> np.ndarray:
        """
        Estimate the phase.

        Returns:
            np.ndarray: the estimated phase.
        """


class NoneBaseEstimator(BasePhaseEstimator):
    """
    NoneBaseEstimator.

    Raise a non implemented error.
    """

    def estimate_phase(self):
        raise NotImplementedError("NoneBaseEstimator should not be used in the DSP.")
