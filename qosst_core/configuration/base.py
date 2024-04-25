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
Abstract class for QOSST Configuration.
"""
import abc
from typing import Dict


# pylint: disable=too-few-public-methods
class BaseConfiguration(abc.ABC):
    """
    Base Configuration object for QOSST (Abstract).
    """

    def __init__(self, config: Dict) -> None:
        """
        Args:
            config (Dict): dict corresponding to one the section in the configuration.
        """
        self.from_dict(config)

    @abc.abstractmethod
    def from_dict(self, config: Dict) -> None:
        """Import the configuration from a dictionnary (TOML).

        Args:
            config (Dict): dictionnary holding good part of the configuration.
        """
