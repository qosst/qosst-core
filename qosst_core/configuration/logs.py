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
Configuration for logs section.
"""
import logging

from qosst_core.configuration.exceptions import InvalidConfiguration
from qosst_core.configuration.base import BaseConfiguration


class LogsConfiguration(BaseConfiguration):
    """
    Logs configuration. It should correspond to the logs section.
    """

    logging: bool  #: Logging if True, not logging if False.
    path: str  #: Path of the log file.
    level: int  #: Logs level as int.
    _level_str: str  #: String representing the level, e.g. info, warning...

    DEFAULT_LOGGING: bool = True  #: Default value for logging.
    DEFAULT_PATH: str = "qosst.log"  #: Default path for the log file.
    DEFAULT_LEVEL_STR: str = "info"  #: Default log level.

    AUTHORIZED_LEVELS = (
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    )  #: Possible log levels.

    def from_dict(self, config: dict) -> None:
        """Populate the logs configuration from the logs section.

        Args:
            config (dict): dict corresponding to the logs section.

        Raises:
            InvalidConfiguration: if the log level is not one of the authorized ones.
        """
        self.logging = config.get("logging", self.DEFAULT_LOGGING)
        self.path = config.get("path", self.DEFAULT_PATH)
        self._level_str = config.get("level", self.DEFAULT_LEVEL_STR)

        if self._level_str not in self.AUTHORIZED_LEVELS:
            raise InvalidConfiguration(
                f"Level {self._level_str} is not valid. Valid choices are {self.AUTHORIZED_LEVELS}."
            )

        self.level = logging.getLevelName(self._level_str.upper())

    def __str__(self) -> str:
        res = "========================\n"
        res += "== Logs Configuration ==\n"
        res += "========================\n"
        res += f"Logging : {self.logging}\n"
        res += f"Path : {self.path}\n"
        res += f"Level : {self._level_str}\n"
        return res
