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
Module for the local oscillator configuration.
"""

from qosst_core.configuration.base import BaseConfiguration


class LocalOscillatorConfiguration(BaseConfiguration):
    """
    Local Oscillator configuration. It should correspond to the local_oscillator section.
    """

    shared: bool  #: True is the LO is shared

    DEFAULT_SHARED: bool = False  #: Default value for the sharing.

    def from_dict(self, config: dict) -> None:
        """Fill the instance from a dict.

        Args:
            config (dict): dict corresponding to the local_oscillator section of the configuration file.
        """
        self.shared = config.get("shared", self.DEFAULT_SHARED)

    def __str__(self) -> str:
        res = "====================================\n"
        res += "== Local Oscillator Configuration ==\n"
        res += "====================================\n"
        res += f"Shared : {self.shared}\n"
        return res
