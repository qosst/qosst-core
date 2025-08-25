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
Configuration for the pushkey section.
"""
from typing import Callable, Dict

from qosst_core.utils import get_object_by_import_path
from qosst_core.configuration.exceptions import InvalidConfiguration
from qosst_core.configuration.base import BaseConfiguration


class PushkeyConfiguration(BaseConfiguration):
    """
    Push key configuration. It should correspond to the pushkey section.
    """

    interface: Callable  #: pushkey interface.
    kwargs: Dict  #: Master of the sharing.

    DEFAULT_INTERFACE_STR: str = (
        "qosst_core.key_management.default_push_key"  #: Default str of the interface function.
    )
    DEFAULT_KWARGS: Dict = {}  #: Default value for the kwargs.

    def from_dict(self, config: dict) -> None:
        """Populate instance from dict.

        Args:
            config (dict): part of the configuration corresponding to the clock section.

        Raises:
        """
        interface_str = config.get("interface", self.DEFAULT_INTERFACE_STR)
        try:
            self.interface = get_object_by_import_path(interface_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load function {interface_str}."
            ) from exc

        if not callable(self.interface):
            raise InvalidConfiguration(f"{interface_str} is not callable.")

        self.kwargs = config.get("kwargs", self.DEFAULT_KWARGS)

    def __str__(self) -> str:
        res = "===========================\n"
        res += "== Pushkey Configuration ==\n"
        res += "===========================\n"
        res += f"Interface : {self.interface}\n"
        res += f"Kwargs : {self.kwargs}\n"
        return res
