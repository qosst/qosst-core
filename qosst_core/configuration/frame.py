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
Configuration for the frames.
"""

from typing import Type
from math import gcd
import logging

import numpy as np

from qosst_core.modulation import Modulation
from qosst_core.configuration.exceptions import InvalidConfiguration
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.utils import get_object_by_import_path

logger = logging.getLogger(__name__)


class FramePilotsConfiguration(BaseConfiguration):
    """
    Class holding the configuration for the pilots.
    """

    num_pilots: int  #: Number of pilots.
    frequencies: np.ndarray  #: np array of the frequency of each pilot.
    amplitudes: np.ndarray  #: np array of the amplitude of each pilot.

    DEFAULT_NUM_PILOTS: int = 2  #: Default number of pilots.
    DEFAULT_FREQUENCIES: list = [
        200e6,
        220e6,
    ]  #: Default value for the list of frequencies.
    DEFAULT_AMPLITUDES: list = [0.4, 0.4]

    def from_dict(self, config: dict) -> None:
        """Fill instance from a dict. It should correspond to the frame.pilots section.

        Args:
            config (dict): dict corresponding to the frame.pilots section.

        Raises:
            InvalidConfiguration: If the length of the frequencies array is not the same as the number of pilots.
            InvalidConfiguration: If the length of the amplitudes array is not the same as the number of pilots.
        """
        self.num_pilots = config.get("num_pilots", self.DEFAULT_NUM_PILOTS)
        self.frequencies = np.array(config.get("frequencies", self.DEFAULT_FREQUENCIES))
        self.amplitudes = config.get("amplitudes", self.DEFAULT_AMPLITUDES)

        if len(self.frequencies) != self.num_pilots:
            raise InvalidConfiguration(
                f"You gave {len(self.frequencies)} frequencies and asked for {self.num_pilots} pilots."
            )

        if len(self.amplitudes) != self.num_pilots:
            raise InvalidConfiguration(
                f"You gave {len(self.amplitudes)} amplitudes and asked for {self.num_pilots} pilots."
            )

    def __str__(self) -> str:
        res = "Frame Pilots Configuration\n"
        res += "--------------------------\n"
        res += f"Num pilots : {self.num_pilots}\n"
        res += f"Frequencies : {self.frequencies*1e-6} Mhz\n"
        res += f"Amplitudes : {self.amplitudes}\n"
        return res


# pylint: disable=too-many-instance-attributes
class FrameQuantumConfiguration(BaseConfiguration):
    """
    Class holding the configuration for the Quantum Data. It should correspond to the frame.quantum section.
    """

    num_symbols: int  #: Number of symbols for quantum data
    frequency_shift: float  #: Center frequency of the quantum data
    pulsed: bool  #: If true, use a rectangular filter instead of a root raised cosine filter.
    symbol_rate: int  #: Symbol rate
    roll_off: float  #: Roll off factor of the root raised cosine filter
    variance: float  #: Variance of the quantum data compared to the tone (modulus of 1)
    modulation_cls: Type[Modulation]  #: Modulation type
    modulation_size: int  #: Size of the modulation

    DEFAULT_NUM_SYMBOLS: int = 1000000  #: Default value for the number of symbols
    DEFAULT_PULSED: bool = False  #: Default value for the pulsed behavior.
    DEFAULT_FREQUENCY_SHIFT: float = 100e6  #: Default value for the center frequency
    DEFAULT_SYMBOL_RATE: float = 100e6  #: Default value for the symbol rate
    DEFAULT_ROLL_OFF: float = 0.5  #: Default value for the roll off factor
    DEFAULT_VARIANCE: float = 0.01  #: Default value for the variance
    DEFAULT_MODULATION_STR: str = (
        "qosst_core.modulation.GaussianModulation"  #: Default modulation
    )
    DEFAULT_MODULATION_SIZE: int = 0  #: Default value for the size of modulation

    def from_dict(self, config: dict) -> None:
        """Fill the instance from a dict.

        Args:
            config (dict): Corresponds to the frame.quantum section

        Raises:
            InvalidConfiguration: If the given modulation class is not a subclass of :class:`~cvqkd_core.modulation.Modulation`
            InvalidConfiguration: If the modulation class does not exist in `cvqkd_core.modulation`.
            InvalidConfiguration: If the roll off factor is not between 0 and 1.
        """
        self.num_symbols = config.get("num_symbols", self.DEFAULT_NUM_SYMBOLS)
        self.frequency_shift = config.get(
            "frequency_shift", self.DEFAULT_FREQUENCY_SHIFT
        )
        self.pulsed = config.get("pulsed", self.DEFAULT_PULSED)
        self.symbol_rate = int(config.get("symbol_rate", self.DEFAULT_SYMBOL_RATE))
        self.roll_off = config.get("roll_off", self.DEFAULT_ROLL_OFF)
        self.variance = config.get("variance", self.DEFAULT_VARIANCE)
        modulation_str = config.get("modulation_type", self.DEFAULT_MODULATION_STR)
        try:
            self.modulation_cls = get_object_by_import_path(modulation_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load modulation class {modulation_str}."
            ) from exc

        if not issubclass(self.modulation_cls, Modulation):
            raise InvalidConfiguration(
                f"The modulation class {modulation_str} is not a subclass of qosst_core.modulation.Modulation."
            )

        self.modulation_size = config.get(
            "modulation_size", self.DEFAULT_MODULATION_SIZE
        )

        if not 0 <= self.roll_off <= 1:
            raise InvalidConfiguration(
                f"The Roll Off value must be between 0 and 1 (given value : {self.roll_off})"
            )

    def __str__(self) -> str:
        res = "Frame QI Configuration\n"
        res += "----------------------\n"
        res += f"Num symbols : {self.num_symbols}\n"
        res += f"Pulsed : {self.pulsed}\n"
        res += f"Frequency shift : {self.frequency_shift*1e-6} MHz\n"
        res += f"Symbol rate : {self.symbol_rate*1e-6} MBaud\n"
        res += f"Roll off : {self.roll_off}\n"
        res += f"Variance : {self.variance}\n"
        res += f"Modulation type : {self.modulation_cls.__name__}\n"
        res += f"Modulation size : {self.modulation_size}\n"
        return res


class FrameZadoffChuConfiguration(BaseConfiguration):
    """
    Configuration of the Zadoff-Chu sequence. It should correspond to the frame.zadoff_chu section.
    """

    root: int  #: Root value for the Zadoff-Chu Sequence
    length: int  #: Length of the Zadoff-Chu sequence
    rate: float  #: Rate of the Zadoff-Chu sequence. A rate of zero will be understood as the same rate as the DAC.

    DEFAULT_ROOT: int = 5  #: Default value for the root.
    DEFAULT_LENGTH: int = 3989  #: Default value for the length.
    DEFAULT_RATE: float = 0  #: Default rate.

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict.

        Args:
            config (dict): dict corresponding to the frame.zadoff_chu section.

        Raises:
            InvalidConfiguration: If the root and length of the Zadoff-Chu sequence are not coprimes.
        """
        self.root = config.get("root", self.DEFAULT_ROOT)
        self.length = config.get("length", self.DEFAULT_LENGTH)
        self.rate = config.get("rate", self.DEFAULT_RATE)

        if not gcd(self.root, self.length) == 1:
            raise InvalidConfiguration(
                f"The root and length of the Zadoff-Chu sequence should be coprimes (gcd = {gcd(self.root, self.length)})"
            )

    def __str__(self) -> str:
        res = "Frame ZC Configuration\n"
        res += "----------------------\n"
        res += f"Root : {self.root}\n"
        res += f"Length : {self.length}\n"
        res += f"Rate : {self.rate}\n"
        return res


class FrameConfiguration(BaseConfiguration):
    """
    The configuration holding the frame configuration.

    In particular this holds three importants configuration :

        * Pilots
        * Quantum Data
        * Zadoff-Chu
    """

    num_zeros_start: int  #: Number of zeros to add at the start of the sequence
    num_zeros_end: int  #: Number of zeros to add at the end of the sequence
    pilots: FramePilotsConfiguration  #: Pilots configuration
    quantum: FrameQuantumConfiguration  #: Quantum Data configuration
    zadoff_chu: FrameZadoffChuConfiguration  #: Zadoff-Chu configuration

    DEFAULT_NUM_ZEROS_START: int = 0  #: Default number of zeros in the start
    DEFAULT_NUM_ZEROS_END: int = 0  #: Default number of zeros in the end

    def from_dict(self, config: dict) -> None:
        """Fill the instance from a dict.

        Args:
            config (dict): dict corresponding to the frame section of the configuration file.
        """
        if not "pilots" in config:
            logger.warning(
                "frame.pilots is missing from the configuration file. Using default values for all the parameters."
            )

        if not "quantum" in config:
            logger.warning(
                "frame.quantum is missing from the configuration file. Using default values for all the parameters."
            )

        if not "zadoff_chu" in config:
            logger.warning(
                "frame.zadoff_chu is missing from the configuration file. Using default values for all the parameters."
            )

        self.num_zeros_start = config.get(
            "num_zeros_start", self.DEFAULT_NUM_ZEROS_START
        )
        self.num_zeros_end = config.get("num_zeros_end", self.DEFAULT_NUM_ZEROS_END)
        self.pilots = FramePilotsConfiguration(config.get("pilots", {}))
        self.quantum = FrameQuantumConfiguration(config.get("quantum", {}))
        self.zadoff_chu = FrameZadoffChuConfiguration(config.get("zadoff_chu", {}))

    def __str__(self) -> str:
        res = "=========================\n"
        res += "== Frame Configuration ==\n"
        res += "=========================\n"
        res += f"Number of zeros in start : {self.num_zeros_start}\n"
        res += f"Number of zeros in end : {self.num_zeros_end}\n"
        res += "\n"
        res += str(self.pilots)
        res += "\n"
        res += str(self.quantum)
        res += "\n"
        res += str(self.zadoff_chu)
        res += "\n"
        return res
