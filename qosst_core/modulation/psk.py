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


class PSKModulation(DiscreteModulation):
    """
    Phase Shift Keying modulation with modulation_size points.

    modulation_size should be a power of 2.
    """

    def __init__(self, variance: float, modulation_size: int) -> None:
        """
        Args:
            variance (float): variance of the modulation.
            modulation_size (int): size of the PSK.

        Raises:
            ValueError: if the modulation size is not a power of 2.
        """
        if int(np.log2(modulation_size)) != np.log2(modulation_size):
            raise ValueError(
                f"modulation_size should be a power of 2 (m = {modulation_size})"
            )

        constellation = np.exp(
            1j * 2 * np.pi / modulation_size * np.arange(modulation_size)
        )
        constellation = constellation * np.sqrt(
            variance / (2 * np.mean(np.abs(constellation) ** 2))
        )

        super().__init__(variance, constellation, None)

    def __repr__(self) -> str:
        return f"PSKModulation(Va={self.variance}, M={len(self.constellation)})"

    def __str__(self) -> str:
        return f"PSK modulation (Va = {self.variance}, M = {len(self.constellation)})"
