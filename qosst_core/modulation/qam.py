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
QAM modulation.
"""
from itertools import product
import numpy as np

from qosst_core.modulation.modulation import DiscreteModulation


class QAMModulation(DiscreteModulation):
    """
    Quadrature Amplitude Modulation with modulation_size points.

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

        quadrature = range(
            -int(modulation_size**0.5) + 1,
            int(modulation_size**0.5),
            2,
        )

        constellation = np.array(
            [x + 1j * y for x, y in product(quadrature, quadrature)]
        )
        constellation = constellation * np.sqrt(
            variance / (2 * np.mean(np.abs(constellation) ** 2))
        )

        super().__init__(variance, constellation, None)

    def __repr__(self) -> str:
        return f"QAMModulation(variance={self.variance}, modulation_size={len(self.constellation)})"

    def __str__(self) -> str:
        return f"QAM modulation (Va = {self.variance}, M = {len(self.constellation)})"
