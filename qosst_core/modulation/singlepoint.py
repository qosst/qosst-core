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
PSK modulation.
"""
import numpy as np

from qosst_core.modulation.modulation import DiscreteModulation


class SinglePointModulation(DiscreteModulation):
    """
    Single point modulation.
    """

    real: float  #: Real value of the point.
    imag: float  #: Imaginary value of the point.

    def __init__(
        self,
        **kwargs,
    ) -> None:
        """
        Variance and modulation_size can be set for convenience.

        Args:
            real (float, optional): value of the real part of the point. Defaults to 1.
            imag (float, optional): value of the imaginary part of the point. Defaults to 1.
        """
        self.real = kwargs.get("real", 1)
        self.imag = kwargs.get("imag", 1)
        constellation = np.array([self.real + 1j * self.imag])
        super().__init__(0, constellation, None)

    def __repr__(self) -> str:
        return f"SinglePointModulation(variance={self.variance}, _modulation_size={len(self.constellation)}, real={self.real}, imag={self.imag})"

    def __str__(self) -> str:
        return f"Single point modulation (Va = {self.variance}, real = {self.real}, imag = {self.imag})"
