# qosst-core - Core module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2025 Yoann Piétri

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
QOSST module for random number generation.
"""

import abc
from typing import Tuple, Optional

import numpy as np


class RandomnessSource(abc.ABC):
    """
    Base class for randomness sources. Implement a binormal method and choice method.
    """

    def __init__(self, **kwargs):
        super().__init__()

    @abc.abstractmethod
    def binormal(self, loc=0, scale=1, size=1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return two independent numpy arrays following the same normal distribution
        with location loc and scale scale (each of them with size samples).

        Args:
            loc (int, optional): mean value for the normal distribution. Defaults to 0.
            scale (int, optional): standard deviation for the normal distribution. Defaults to 1.
            size (int, optional): number of samples in each resulting arrays.. Defaults to 1.

        Returns:
            Tuple[np.ndarray, np.ndarray]: the two normal arrays.
        """

    @abc.abstractmethod
    def choice(
        self, constellation: np.ndarray, size=1, p: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Return an array of points from the constellation with size samples, the
        sampling being done following the distribution in p. If p is None, the
        uniform distribution is assumed.

        Args:
            constellation (np.ndarray): array of possible points.
            size (int, optional): number of samples to generate. Defaults to 1.
            p (np.ndarray, optional): distribution to choose from the constellation. If None, uses the uniform distribution. Defaults to None.

        Returns:
            np.ndarray: the sampled points from the constellation.
        """


class NumpyRandomnessSource(RandomnessSource):
    """
    A randomness source based on numpy.
    """

    def binormal(self, loc=0, scale=1, size=1):
        return (
            np.random.normal(loc=loc, scale=scale, size=size),
            np.random.normal(loc=loc, scale=scale, size=size),
        )

    def choice(self, constellation, size=1, p=None):
        return np.random.choice(constellation, size=size, p=p)
