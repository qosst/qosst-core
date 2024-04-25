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
Configuration for the clock section.
"""
from qosst_core.configuration.exceptions import InvalidClockMaster
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.participant import Participant


class ClockConfiguration(BaseConfiguration):
    """
    Clock configuration. It should correspond to the clock section.
    """

    sharing: bool  #: True if clock is shared. False otherwise.
    master: Participant  #: Master of the sharing.

    DEFAULT_SHARING: bool = False  #: Default value for sharing.
    DEFAULT_MASTER: str = "alice"  #: Default value for master.

    def from_dict(self, config: dict) -> None:
        """Populate instance from dict.

        Args:
            config (dict): part of the configuration corresponding to the clock section.

        Raises:
            InvalidClockMaster: if the clock master is not alice or bob.
        """
        self.sharing = config.get("sharing", self.DEFAULT_SHARING)
        try:
            self.master = Participant(config.get("master", self.DEFAULT_MASTER))
        except ValueError as exc:
            raise InvalidClockMaster(config.get("master", self.DEFAULT_MASTER)) from exc

    def __str__(self) -> str:
        res = "=========================\n"
        res += "== Clock Configuration ==\n"
        res += "=========================\n"
        res += f"Sharing : {self.sharing}\n"
        res += f"Master : {self.master}\n"
        return res
