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
Configuration for the channel section.
"""
from typing import Dict, Type
import logging

from qosst_hal.voa import GenericVOA
from qosst_core.configuration.exceptions import (
    InvalidConfiguration,
)
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.utils import get_object_by_import_path
from qosst_core.participant import Participant

logger = logging.getLogger(__name__)


class ChannelVOAConfiguration(BaseConfiguration):
    """
    Configuration to use a Variable Optical Attenuator as a channel. This is useful for some tests.
    It should correspond to the channel.voa section.
    """

    use: bool  #: Use the VOA as a channel.
    applier: Participant  #: Which participant has control over the VOA.
    device: Type[GenericVOA]  #: The device class of the VOA.
    location: str  #: The location of the VOA.
    value: float  #: The value to apply to the VOA.
    extra_args: Dict  #: Som extra arguments for the VOA.

    DEFAULT_USE: bool = False  #: Default value for use.
    DEFAULT_APPLIER_STR: str = "alice"  #: Default applier (as a string).
    DEFAULT_DEVICE_STR: str = (
        "qosst_hal.voa.FakeVOA"  #: Default VOA class (as a string).
    )
    DEFAULT_LOCATION: str = ""  #: Default location of the VOA.
    DEFAULT_VALUE: float = 0  #: Default value to apply to the VOA.
    DEFAULT_EXTRA_ARGS: Dict = {}  #: Default extra arguments.

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict.

        Args:
            config (dict): dict correspoding to the channel.voa section.

        Raises:
            InvalidConfiguration: if the applier is not a valid choice (alice or bon)
            InvalidConfiguration: if the device class canoot be loaded.
            InvalidConfiguration: if the device class is noit a subclass of :class:`qosst_hal.voa.GenericVOA`.
        """
        self.use = config.get("use", self.DEFAULT_USE)
        applier_str = config.get("applier", self.DEFAULT_APPLIER_STR)
        try:
            self.applier = Participant(applier_str)
        except ValueError as exc:
            raise InvalidConfiguration(
                f"{applier_str} is not a valid applier."
            ) from exc
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Impossible to load the VOA device {device_str}."
            ) from exc

        if not issubclass(self.device, GenericVOA):
            raise InvalidConfiguration(f"{device_str} is not a subclass of GenericVOA.")

        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.value = config.get("value", self.DEFAULT_VALUE)
        self.extra_args = config.get("extra_args", self.DEFAULT_EXTRA_ARGS)

    def __str__(self) -> str:
        res = "Channel VOA Configuration\n"
        res += "-------------------------\n"
        res += f"Use : {self.use}\n"
        res += f"Applier : {self.applier}\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += f"Value : {self.value}\n"
        res += f"Extra args : {self.extra_args}\n"
        res += "\n"
        return res


class ChannelConfiguration(BaseConfiguration):
    """
    The channel configuration. It should correspond to the channel section.
    """

    voa: ChannelVOAConfiguration  #: The channel VOA configuration.

    def from_dict(self, config: dict) -> None:
        """Fill instance from the config.

        Args:
            config (dict): dict corresponding to the channel section.
        """
        if "voa" not in config:
            logger.warning(
                "channel.voa is missing from the configuration file. Using default values for all the parameters."
            )

        self.voa = ChannelVOAConfiguration(config.get("network", {}))

    def __str__(self) -> str:
        res = "===========================\n"
        res += "== Channel Configuration ==\n"
        res += "===========================\n"
        res += str(self.voa)
        return res
