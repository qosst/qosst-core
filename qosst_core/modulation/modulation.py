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
Generic modulation.
"""
import abc
from typing import Optional

import numpy as np
from qosst_core.utils import bitarray_to_decimal, decimal_to_bitarray


# pylint: disable=too-few-public-methods
class Modulation(abc.ABC):
    """
    Abstract class for the modulations.
    """

    variance: float  #: variance of the modulation.

    def __init__(self, variance: float, **_kwargs) -> None:
        """
        Args:
            variance (float): variance of the modulation.
        """
        self.variance = variance

    @abc.abstractmethod
    def modulate(self, size: int) -> np.ndarray:
        """
        Modulate and return an array containing the symbols.

        Args:
            size (int): number of points to modulate.

        Returns:
            np.ndarray: the modulated points.
        """


class DiscreteModulation(Modulation, abc.ABC):
    """
    Abstract class representing a discrete modulation.

    In particular it contains the constellation (i.e. an array
    of the possible symbols) and a distribution (i.e. the
    associated array of probability of those symbols).
    """

    constellation: np.ndarray  #: Possible symbols of the modulation.
    distribution: Optional[
        np.ndarray
    ]  #: Probabilities associated to those symbols. None should be considered the uniform distribution.

    def __init__(
        self,
        variance: float,
        constellation: np.ndarray,
        distribution: Optional[np.ndarray],
    ) -> None:
        """
        Args:
            variance (float): variance of the modulation.
            constellation (np.ndarray): constellation (array of possible symbols).
            distribution (np.ndarray): distribution (array of probability of those symbols).
        """
        self.constellation = constellation
        self.distribution = distribution
        super().__init__(variance)

    def bits_to_symbols(self, input_bits: np.ndarray) -> np.ndarray:
        """
        Modulate the bits according to the modulation.

        Args:
            input_bits (np.ndarray): array of input bits.

        Returns:
            np.ndarray: array of output symbols.
        """
        num_bits_symbol = int(np.log2(len(self.constellation)))
        mapfunc = np.vectorize(
            lambda i: self.constellation[
                bitarray_to_decimal(input_bits[i : i + num_bits_symbol])
            ]
        )

        baseband_symbols = mapfunc(np.arange(0, len(input_bits), num_bits_symbol))

        return baseband_symbols

    def nearest_point(self, input_symbols: np.ndarray) -> np.ndarray:
        """
        Find the nearest point in the constellation of any given point.

        Args:
            input_symbols (np.ndarray): array of input imperfect symbols.

        Returns:
            np.ndarray: array of perfect outputs symbols.
        """
        return abs(input_symbols - self.constellation[:, None]).argmin(0)

    def symbols_to_bits(self, input_symbols: np.ndarray) -> np.ndarray:
        """
        Demodulate symbols according to the modulation.

        Args:
            input_symbols (np.ndarray): array of input symbols.

        Returns:
            np.ndarray: array of output bits.
        """
        num_bits_symbol = int(np.log2(len(self.constellation)))
        index_list = self.nearest_point(input_symbols)
        demod_bits = decimal_to_bitarray(index_list, num_bits_symbol)
        return demod_bits

    def modulate(self, size: int) -> np.ndarray:
        """Generate an array of size size, containing symbols from the constellation
        and following the distribution of probability.

        Args:
            size (int): number of symbols to generate.

        Returns:
            np.ndarray: array of symbols, of size size.
        """
        return np.random.choice(self.constellation, size=size, p=self.distribution)
