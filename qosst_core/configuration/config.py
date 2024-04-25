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
This is the definition of configuration classes for QOSST.

Each class corresponds to a section in the .toml configuration file.

The mean configuration class is parent to the other configuration classes.
"""

from typing import Optional
import logging

import toml

from qosst_core.configuration.logs import LogsConfiguration
from qosst_core.configuration.alice import AliceConfiguration
from qosst_core.configuration.bob import BobConfiguration
from qosst_core.configuration.frame import FrameConfiguration
from qosst_core.configuration.clock import ClockConfiguration
from qosst_core.configuration.local_oscillator import LocalOscillatorConfiguration
from qosst_core.configuration.authentication import AuthenticationConfiguration
from qosst_core.configuration.exceptions import InvalidConfiguration
from qosst_core.configuration.notifications import NotificationsConfiguration
from qosst_core.configuration.channel import ChannelConfiguration
from qosst_core.utils import QOSSTPath

logger = logging.getLogger(__name__)


class PickleableTomlDecoder(toml.TomlDecoder):
    """
    For some reason (see https://github.com/uiri/toml/issues/362),
    the default toml decoder is not piclkable only because of the get_empty_inline_table
    function.

    Therefore, we take the solution proposed in the issue to make it pickable.
    """

    def get_empty_inline_table(self):
        """
        Reimplementation of the get_empty_inline_table to be pickable.
        """
        return self.get_empty_table()


# pylint: disable=too-many-instance-attributes, too-many-branches
class Configuration:
    """
    The main class of the configuration.

    The configuration file should be a valid toml file.

    Example of use :

    .. code-block::

        c = Configuration("config.toml")
        print(c.label)
        print(c.alice.network.address)
    """

    _config_path: QOSSTPath  #: Initial path of the configuration
    _config: Optional[dict]  #: dict representing the configuration
    label: str  #: label of the configuration
    serial_number: str  #: Serial number of the machine.
    logs: LogsConfiguration  #: Logs configuration.
    notifications: Optional[NotificationsConfiguration]  #: Notifications configuration.
    authentication: Optional[
        AuthenticationConfiguration
    ]  #: Authentication configuration.
    clock: Optional[ClockConfiguration]  #: Clock configuration.
    channel: Optional[ChannelConfiguration]  #: Channel configuration.
    local_oscillator: Optional[
        LocalOscillatorConfiguration
    ]  #: Local Oscillator configuration.
    alice: Optional[AliceConfiguration]  #: Alice configuration.
    bob: Optional[BobConfiguration]  #: Bob configuration.
    frame: Optional[FrameConfiguration]  #: Frame configuration.

    DEFAULT_LABEL: str = "Example config"  #: Default label
    DEFAULT_SERIAL_NUMBER: str = ""

    def __init__(self, config_path: QOSSTPath) -> None:
        """
        Args:
            config_path (QOSSTPath): path of the configuration file.
        """
        self._config_path = config_path
        self._config = None

        try:
            config = toml.load(str(config_path), decoder=PickleableTomlDecoder())
        except toml.TomlDecodeError as exc:
            raise InvalidConfiguration("The TOML file is not readable.") from exc

        self.from_dict(config)

    def to_dict(self) -> Optional[dict]:
        """
        Return config as a dict.

        Returns:
            dict: dict holding the config.
        """
        return self._config

    def from_dict(self, config: dict) -> None:
        """Fill the config from a dict. It should corresond to the configuration file.

        This dict can come from a toml file or from another party.

        If the current config is being overwritten, a warning message is issued.
        Please note here that, for now, the message is issued even if the difference
        come from sections that will not be overwritten (for instance, if alice section
        is not present in the overwriting configuration, the alice configuration in the
        class will not be set to None).

        Args:
            config (dict): the dict holding the config.
        """
        if config != self._config and self._config is not None:
            logger.warning("Overwriting config.")
        self._config = config
        self.label = config.get("label", self.DEFAULT_LABEL)
        self.serial_number = config.get("serial_number", self.DEFAULT_SERIAL_NUMBER)

        if "logs" not in config:
            logger.warning(
                "The logs sections is not present in the configuration file. Using default values for all parameters."
            )

        self.logs = LogsConfiguration(config.get("logs", {}))

        if "notifications" in config:
            self.notifications = NotificationsConfiguration(config["notifications"])
        else:
            self.notifications = None

        if "authentication" in config:
            self.authentication = AuthenticationConfiguration(config["authentication"])
        else:
            self.authentication = None

        if "clock" in config:
            self.clock = ClockConfiguration(config["clock"])
        else:
            self.clock = None

        if "channel" in config:
            self.channel = ChannelConfiguration(config["channel"])
        else:
            self.channel = None

        if "local_oscillator" in config:
            self.local_oscillator = LocalOscillatorConfiguration(
                config["local_oscillator"]
            )
        else:
            self.local_oscillator = None

        if "alice" in config:
            self.alice = AliceConfiguration(config["alice"])
        else:
            self.alice = None

        if "bob" in config:
            self.bob = BobConfiguration(config["bob"])
        else:
            self.bob = None

        if "frame" in config:
            self.frame = FrameConfiguration(config["frame"])
        else:
            self.frame = None

    def __repr__(self) -> str:
        return f'Configuration("{self._config_path}")'

    def __str__(self) -> str:
        res = f"Configuration : {self.label} (Loaded from : {self._config_path})\n"
        res += f"Serial number : {self.serial_number}\n"
        res += "\n"
        res += str(self.logs)
        res += "\n"
        res += str(self.notifications)
        res += "\n"
        res += str(self.authentication)
        res += "\n"
        res += str(self.clock)
        res += "\n"
        res += str(self.channel)
        res += "\n"
        res += str(self.local_oscillator)
        res += "\n"
        res += str(self.alice)
        res += "\n"
        res += str(self.bob)
        res += "\n"
        res += str(self.frame)
        return res
