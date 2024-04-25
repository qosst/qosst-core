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
from itertools import product
import numpy as np

from qosst_core.modulation.qam import DiscreteModulation


class PCSQAMModulation(DiscreteModulation):
    """Quadrature Amplitude Modulation with modulation_size points,
    using Probabilistic Constellation Shaping.

    modulation_size should be a power of 2 and a square.
    """

    nu: float  #: Parameter for the distribution of probbaility.

    def __init__(self, variance: float, modulation_size: int, nu: float) -> None:
        """
        The distribution is choosen to be (before normalization)

        p(x,y) = exp(-nu*(x**2+y**2))

        Args:
            variance (float): variance of the modulation.
            modulation_size (int): size of the QAM.
            nu (float): parameter for the distribution of probability.

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
        distribution = np.exp(-nu * abs(constellation) ** 2) / sum(
            np.exp(-nu * abs(constellation) ** 2)
        )
        constellation = constellation * np.sqrt(
            variance / (2 * np.dot(np.abs(constellation) ** 2, distribution))
        )
        self.nu = nu

        super().__init__(variance, constellation, distribution)

    def __repr__(self) -> str:
        return f"PCSQAMModulation(variance={self.variance}, modulation_size={len(self.constellation)}, nu={self.nu})"

    def __str__(self) -> str:
        return f"PCS-QAM modulation (Modulation size = {len(self.constellation)}, Va = {self.variance}, nu = {self.nu})"
