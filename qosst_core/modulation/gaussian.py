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
Gaussian modulation.
"""
import numpy as np

from .modulation import Modulation


class GaussianModulation(Modulation):
    """
    Gaussian modulation.
    """

    def __init__(self, variance: float, **_kwargs) -> None:
        """
        Args:
            variance (float): variance of the gaussian modulation.
        """
        super().__init__(variance)

    def modulate(self, size: int) -> np.ndarray:
        """Modulate from the modulation.

        Args:
            size (int): Number of symbols to output.

        Returns:
            np.ndarray: size symbols from a Gaussian distribution on each quadrature.
        """
        return np.random.normal(
            loc=0, scale=np.sqrt(self.variance), size=(size,)
        ) + 1j * np.random.normal(loc=0, scale=np.sqrt(self.variance), size=(size,))

    def __repr__(self) -> str:
        return f"GaussianModulation(Va={self.variance})"

    def __str__(self) -> str:
        return f"Gaussian modulation (Va = {self.variance})"
