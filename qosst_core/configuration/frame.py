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
from qosst_core.synchronization import SynchronizationSequence
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


class FrameSynchronizationConfiguration(BaseConfiguration):
    """
    Configuration of the synchronization sequence. It should correspond to the frame.synchronization section.
    """

    synchronization_cls: Type[
        SynchronizationSequence
    ]  #: Synchronization sequence class.
    zc_root: int  #: Root value for the Zadoff-Chu Sequence.
    zc_length: int  #: Length of the Zadoff-Chu sequence.
    mls_nbits: int  #: Number of bits of the Maximum Length Sequence.
    rate: float  #: Rate of the Zadoff-Chu sequence. A rate of zero will be understood as the same rate as the DAC.
    amplitude: float  #: Amplitude of the Zadoff-Chu sequence. An amplitude of 1.0 means that the sequence is output at the maximum amplitude of the DAC.

    DEFAULT_SYNCHRONIZATION_STR: str = (
        "qosst_core.synchronization.ZadoffChuSequence"  #: Default synchronization.
    )
    DEFAULT_ZC_ROOT: int = 5  #: Default value for the root of the Zadoff-Chu sequence.
    DEFAULT_ZC_LENGTH: int = (
        3989  #: Default value for the length of the Zadoff-Chu sequence.
    )
    DEFAULT_MLS_NBITS: int = (
        16  #: Default value for the number of bits of the Maximum Length Sequence.
    )
    DEFAULT_RATE: float = 0  #: Default rate.
    DEFAULT_AMPLITUDE: float = 1  #: Default amplitude of the synchronization sequence.

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict.

        Args:
            config (dict): dict corresponding to the frame.zadoff_chu section.

        Raises:
            InvalidConfiguration: If the root and length of the Zadoff-Chu sequence are not coprimes.
            InvalidConfiguration: If the rate is less than zero.
            InvalidConfiguration: If the amplitude is not between 0 and 1.
            InvalidConfiguration: If the given synchronization class is not a subclass of :class:`~qosst_core.synchronization.SynchronizationSequence`
            InvalidConfiguration: If the synchronization class does not exist in `qosst_core.syncrhonization`.
        """
        self.zc_root = config.get("zc_root", self.DEFAULT_ZC_ROOT)
        self.zc_length = config.get("zc_length", self.DEFAULT_ZC_LENGTH)
        self.mls_nbits = config.get("mls_nbits", self.DEFAULT_MLS_NBITS)
        self.rate = config.get("rate", self.DEFAULT_RATE)
        self.amplitude = config.get("amplitude", self.DEFAULT_AMPLITUDE)
        synchronization_str = config.get(
            "synchronization_type", self.DEFAULT_SYNCHRONIZATION_STR
        )
        try:
            self.synchronization_cls = get_object_by_import_path(synchronization_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load synchronization sequence class {synchronization_str}."
            ) from exc

        if not issubclass(self.synchronization_cls, SynchronizationSequence):
            raise InvalidConfiguration(
                f"The synchronization class {synchronization_str} is not a subclass of qosst_core.synchronization.SinchronizationSequence."
            )

        if not gcd(self.zc_root, self.zc_length) == 1:
            raise InvalidConfiguration(
                f"The root and length of the Zadoff-Chu sequence should be coprimes (gcd = {gcd(self.zc_root, self.zc_length)})"
            )

        if not self.rate >= 0:
            raise InvalidConfiguration(
                "The rate of the synchronization sequence must be zero or positive (given value : {self.rate})"
            )

        if not 0 <= self.amplitude <= 1:
            raise InvalidConfiguration(
                f"The amplitude of the configuration sequence must be between 0 and 1 (given value : {self.amplitude})"
            )

    def __str__(self) -> str:
        res = "Frame Synchronization Configuration\n"
        res += "----------------------\n"
        res += f"Sequence : {self.synchronization_cls.__name__}\n"
        res += f"ZC_Root : {self.zc_root}\n"
        res += f"ZC_Length : {self.zc_length}\n"
        res += f"MLS_Nbits : {self.mls_nbits}\n"
        res += f"Rate : {self.rate}\n"
        res += f"Amplitude: {self.amplitude}\n"
        return res


class FrameConfiguration(BaseConfiguration):
    """
    The configuration holding the frame configuration.

    In particular this holds three importants configuration :

        * Pilots
        * Quantum Data
        * Synchronization
    """

    num_zeros_start: int  #: Number of zeros to add at the start of the sequence
    num_zeros_end: int  #: Number of zeros to add at the end of the sequence
    pilots: FramePilotsConfiguration  #: Pilots configuration
    quantum: FrameQuantumConfiguration  #: Quantum Data configuration
    synchronization: FrameSynchronizationConfiguration  #: Synchronization configuration

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

        if not "synchronization" in config:
            logger.warning(
                "frame.synchronization is missing from the configuration file. Using default values for all the parameters."
            )

        self.num_zeros_start = config.get(
            "num_zeros_start", self.DEFAULT_NUM_ZEROS_START
        )
        self.num_zeros_end = config.get("num_zeros_end", self.DEFAULT_NUM_ZEROS_END)
        self.pilots = FramePilotsConfiguration(config.get("pilots", {}))
        self.quantum = FrameQuantumConfiguration(config.get("quantum", {}))
        self.synchronization = FrameSynchronizationConfiguration(
            config.get("synchronization", {})
        )

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
        res += str(self.synchronization)
        res += "\n"
        return res
