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
PCSQAM modulation.
"""
from math import comb
from itertools import product
import numpy as np

from qosst_core.modulation.modulation import DiscreteModulation


class BinomialQAMModulation(DiscreteModulation):
    """
    Quadrature Amplitude Modulation with modulation_size points,
    using Binomial Probabilistic Constellation Shaping.

    modulation_size should be a power of 2 and a square.
    """

    def __init__(self, variance: float, modulation_size: int) -> None:
        """
        Args:
            variance (float): variance of the modulation.
            modulation_size (int): size of the QAM.

        Raises:
            ValueError: if the modulation size is not a power of 2.
            ValueError: if the modulation size is not a perfect square.
        """
        if int(np.log2(modulation_size)) != np.log2(modulation_size):
            raise ValueError(
                f"modulation_size should be a power of 2 (m = {modulation_size})"
            )

        if int(np.sqrt(modulation_size) + 0.5) ** 2 != modulation_size:
            raise ValueError(
                f"modulation should be a perfect square (m = {modulation_size})"
            )
        sqrt_modulation_size = int(modulation_size**0.5)

        quadrature = range(
            -sqrt_modulation_size + 1,
            sqrt_modulation_size,
            2,
        )

        constellation = np.array(
            [x + 1j * y for x, y in product(quadrature, quadrature)]
        )
        distribution = np.array(
            [
                2 ** (-2 * (sqrt_modulation_size - 1))
                * comb(sqrt_modulation_size - 1, k)
                * comb(sqrt_modulation_size - 1, l)
                for k, l in product(
                    range(sqrt_modulation_size), range(sqrt_modulation_size)
                )
            ]
        )
        constellation = constellation * np.sqrt(
            variance / (4 * (sqrt_modulation_size - 1))
        )

        super().__init__(variance, constellation, distribution)

    def __repr__(self) -> str:
        return f"BinomialQAMModulation(variance={self.variance}, modulation_size={len(self.constellation)})"

    def __str__(self) -> str:
        return f"Binomial QAM modulation (Modulation size = {len(self.constellation)}, Va = {self.variance})"
