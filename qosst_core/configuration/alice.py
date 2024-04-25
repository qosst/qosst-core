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
Configuration for Alice section.
"""
from typing import Dict, Type
import logging
from warnings import warn

from qosst_hal.dac import GenericDAC
from qosst_hal.powermeter import GenericPowerMeter
from qosst_hal.voa import GenericVOA
from qosst_hal.modulator_bias_control import GenericModulatorBiasController
from qosst_hal.laser import GenericLaser

from qosst_core.control_protocol import DEFAULT_PORT
from qosst_core.configuration.exceptions import InvalidConfiguration
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.utils import get_object_by_import_path
from qosst_core.schema.emission import EmissionSchema

logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class AliceSignalGenerationConfiguration(BaseConfiguration):
    """
    Class holding Alice's Signal Generation Configuration. It should be initialized with the alice.signal_generation section.
    """

    symbols_path: str  #: Symbols path to load or save.
    final_sequence_path: str  #: Final sequence path to load or save.
    quantum_sequence_path: str  #: Quantum sequence path to save.
    load_symbols: bool  #: Boolean to know if symbols have to be generated or loaded.
    load_final_sequence: (
        bool  #: Boolean to know if the final sequence have to be computed or loaded.
    )
    save_symbols: bool  #: Boolean to know if the symbols have to be saved.
    save_final_sequence: bool  #: Boolean to know if the final sequence has to be saved.
    save_quantum_sequence: (
        bool  #: Boolean to know if the quantum sequence has to be saved.
    )

    DEFAULT_SYMBOLS_PATH: str = "symbols.npy"  #: Default symbols path.
    DEFAULT_FINAL_SEQUENCE_PATH: str = (
        "final_sequence.npy"  #: Default final sequence path.
    )
    DEFAULT_QUANTUM_SEQUENCE_PATH: str = (
        "quantum_sequence.npy"  #: Default quantum sequence path.
    )
    DEFAULT_LOAD_SYMBOLS: bool = False  #: Default value for load symbols.
    DEFAULT_LOAD_FINAL_SEQUENCE: bool = False  #: Default value for load final sequence.
    DEFAULT_SAVE_SYMBOLS: bool = True  #: Default value for save symbols.
    DEFAULT_SAVE_FINAL_SEQUENCE: bool = False  #: Default value for save final sequence.
    DEFAULT_SAVE_QUANTUM_SEQUENCE: bool = (
        False  #: Default value for save quantum sequence.
    )

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict.

        Args:
            config (dict): dict holding the configuration for the alice.signal_generation function.
        """
        self.symbols_path = config.get("symbols_path", self.DEFAULT_SYMBOLS_PATH)
        self.final_sequence_path = config.get(
            "final_sequence_path", self.DEFAULT_FINAL_SEQUENCE_PATH
        )
        self.quantum_sequence_path = config.get(
            "quantum_sequence_path", self.DEFAULT_QUANTUM_SEQUENCE_PATH
        )
        self.load_symbols = config.get("load_symbols", self.DEFAULT_LOAD_SYMBOLS)
        self.load_final_sequence = config.get(
            "load_final_sequence", self.DEFAULT_LOAD_FINAL_SEQUENCE
        )
        self.save_symbols = config.get("save_symbols", self.DEFAULT_SAVE_SYMBOLS)
        self.save_final_sequence = config.get(
            "save_final_sequence", self.DEFAULT_SAVE_FINAL_SEQUENCE
        )
        self.save_quantum_sequence = config.get(
            "save_quantum_sequence", self.DEFAULT_SAVE_QUANTUM_SEQUENCE
        )

    def __str__(self) -> str:
        res = "Alice Signal Generation Configuration\n"
        res += "-------------------------------------\n"
        res += f"Symbols path : {self.symbols_path}\n"
        res += f"Final sequence path : {self.final_sequence_path}\n"
        res += f"Quantum sequence path : {self.quantum_sequence_path}\n"
        res += f"Load symbols : {self.load_symbols}\n"
        res += f"Load final sequence : {self.load_final_sequence}\n"
        res += f"Save symbols : {self.save_symbols}\n"
        res += f"Save final sequence : {self.save_final_sequence}\n"
        res += f"Save quantum sequence : {self.save_quantum_sequence}\n"
        res += "\n"
        return res


class AliceNetworkConfiguration(BaseConfiguration):
    """
    Class holding the configuration for Alice network. It should be intialized with the alice.network section.
    """

    bind_address: str  #: Address on which Alice listens.
    bind_port: int  #: Port on which Alice listens

    DEFAULT_BIND_ADDRESS: str = "127.0.0.1"  #: Default address
    DEFAULT_BIND_PORT: int = DEFAULT_PORT  #: Default port

    def from_dict(self, config: dict) -> None:
        """Fill instance form dict.

        Args:
            config (dict): dict corresponding to the alice.network section.
        """
        self.bind_address = config.get("bind_address", self.DEFAULT_BIND_ADDRESS)
        self.bind_port = config.get("bind_port", self.DEFAULT_BIND_PORT)

    def __str__(self) -> str:
        res = "Alice Network Configuration\n"
        res += "---------------------------\n"
        res += f"Bind address : {self.bind_address}\n"
        res += f"Bind port : {self.bind_port}\n"
        res += "\n"
        return res


class AliceDACConfiguration(BaseConfiguration):
    """
    Class holding the configuration for Alice DAC. It should be initialized with the alice.dac section.
    """

    rate: float  #: Rate of the DAC, in Samples/second.
    amplitude: float  #: Amplitude of the DAC, in V.
    device: Type[GenericDAC]  #: Device class of the DAC.
    channels: list  #: List of channels to use.
    extra_args: dict  #: Extra args to pass to the DAC class.

    DEFAULT_RATE: float = 500e6  #: Default rate in Samples/second.
    DEFAULT_AMPLITUDE: float = 0  #: Default amplitude, in V.
    DEFAULT_DEVICE_STR: str = "qosst_hal.dac.FakeDAC"  #: Default class of the DAC.
    DEFAULT_CHANNELS: list = [0, 1]  #: Default channels to use.
    DEFAULT_EXTRA_ARGS: dict = {}  #: Default extra args for the DAC.

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict.

        Args:
            config (dict): dict corresponding to the alice.dac section

        Raises:
            InvalidConfiguration: if the dac class cannot be loaded.
            InvalidConfiguration: if the dac device is not a subclass of GenericDAC
        """
        self.rate = config.get("rate", self.DEFAULT_RATE)
        self.amplitude = config.get("amplitude", self.DEFAULT_AMPLITUDE)
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(f"Cannot load DAC class {device_str}.") from exc

        if not issubclass(self.device, GenericDAC):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclass of qosst_hal.dac.GenericDAC."
            )

        self.channels = config.get("channels", self.DEFAULT_CHANNELS)
        self.extra_args = config.get("extra_args", self.DEFAULT_EXTRA_ARGS)

    def __str__(self) -> str:
        res = "Alice DAC Configuration\n"
        res += "-----------------------\n"
        res += f"Rate : {self.rate*1e-6} MSamples/s\n"
        res += f"Amplitude : {self.amplitude}\n"
        res += f"Device : {self.device}\n"
        res += f"Channels : {self.channels}\n"
        res += f"Extra args : {self.extra_args}\n"
        res += "\n"
        return res


class AlicePowerMeterConfiguration(BaseConfiguration):
    """
    Configuration for Alice's powermeter section. It should be initialized with the alice.powermeter section.
    """

    device: Type[GenericPowerMeter]  #: Device class to use as powermeter.
    location: str  #: Location of the powermeter
    timeout: int  #: Timeout for the connection

    DEFAULT_DEVICE_STR: str = (
        "qosst_hal.powermeter.FakePowerMeter"  #: Default device class
    )
    DEFAULT_LOCATION: str = ""  #: Default location
    DEFAULT_TIMEOUT: int = 10  #: Default timeout

    def from_dict(self, config: dict):
        """Fill the instance from dict.

        Args:
            config (dict): dict corresponding to the alice.powermeter section.

        Raises:
            InvalidConfiguration: if the powermeter class cannot be loaded.
            InvalidConfiguration: if the device class is not a subclass of GenericPowerMeter.
        """
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load powermeter class {device_str}."
            ) from exc

        if not issubclass(self.device, GenericPowerMeter):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclasse of qosst_hal.powermeter.GenericPowerMeter."
            )
        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.timeout = config.get("timeout", self.DEFAULT_TIMEOUT)

    def __str__(self) -> str:
        res = "Alice PowerMeter Configuration\n"
        res += "------------------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += f"Timeout : {self.timeout}\n"
        res += "\n"
        return res


class AliceVOAConfiguration(BaseConfiguration):
    """
    Configuration for Alice's VOA section. It should be initialized with the alice.voa section.
    """

    device: Type[GenericVOA]  #: Device class to use as VOA.
    location: str  #: Location of the VOA
    value: float  #: Value to apply to the VOA.
    extra_args: dict  #: Extra args to pass to the VOA.

    DEFAULT_DEVICE_STR: str = "qosst_hal.voa.FakeVOA"  #: Default device class
    DEFAULT_LOCATION: str = ""  #: Default location
    DEFAULT_VALUE: float = 0  #: Default value to apply to the VOA.
    DEFAULT_EXTRA_ARGS: dict = {}  #: Default extra args to pass as parameters.

    def from_dict(self, config: dict):
        """Fill the instance from dict.

        Args:
            config (dict): dict corresponding to the alice.voa section.

        Raises:
            InvalidConfiguration: if the voa class cannot be loaded.
            InvalidConfiguration: if the device class is not a subclass of GenericVOA.
        """
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(f"Cannot load VOA class {device_str}.") from exc

        if not issubclass(self.device, GenericVOA):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclasse of qosst_hal.voa.GenericVOA."
            )
        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.value = config.get("value", self.DEFAULT_VALUE)
        self.extra_args = config.get("extra_args", self.DEFAULT_EXTRA_ARGS)

    def __str__(self) -> str:
        res = "Alice VOA Configuration\n"
        res += "-----------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += f"Value : {self.value}\n"
        res += f"Extra args : {self.extra_args}\n"
        res += "\n"
        return res


class AliceModulatorBiasControlConfiguration(BaseConfiguration):
    """Configuration for Alice's bias modulator section. It should be intialized with the alice.modulator_bias_control section."""

    device: Type[
        GenericModulatorBiasController
    ]  #: Device class to use as bias controller.
    location: str  #: Location of the bias controller.
    extra_args: dict  #: Extra args to pass to the bias controller.

    DEFAULT_DEVICE_STR: str = (
        "qosst_hal.modulator_bias_control.FakeModulatorBiasController"  #: Default device class
    )
    DEFAULT_LOCATION: str = ""  #: Default location
    DEFAULT_EXTRA_ARGS: dict = {}  #: Default extra args to pass as parameters.

    def from_dict(self, config: dict):
        """Fill the instance from dict.

        Args:
            config (dict): dict corresponding to the alice.modulator_bias_control section.

        Raises:
            InvalidConfiguration: if the device class cannot be loaded.
            InvalidConfiguration: if the device class is not a subclass of GenericModulatorBiasController.
        """
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load bias controller class {device_str}."
            ) from exc

        if not issubclass(self.device, GenericModulatorBiasController):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclasse of qosst_hal.modulator_bias_control.GenericModulatorBiasController."
            )
        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.extra_args = config.get("extra_args", self.DEFAULT_EXTRA_ARGS)

    def __str__(self) -> str:
        res = "Alice bias controller Configuration\n"
        res += "-----------------------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += f"Extra args : {self.extra_args}\n"
        res += "\n"
        return res


class AliceLaserConfiguration(BaseConfiguration):
    """
    Configuration for Alice's laser section. It should be loaded with the alice.laser section.
    """

    device: Type[GenericLaser]  #: Device class to use as laser.
    location: str  #: Location of the laser.
    parameters: dict  #: Parameters to pass to the laser.

    DEFAULT_DEVICE_STR: str = "qosst_hal.laser.FakeLaser"  #: Default device class
    DEFAULT_LOCATION: str = ""  #: Default location
    DEFAULT_PARAMETERS: dict = {}  #: Default parameters to pass to the laser.

    def from_dict(self, config: dict):
        """Fill the instance from dict.

        Args:
            config (dict): dict corresponding to the alice.laser section.

        Raises:
            InvalidConfiguration: if the device class cannot be loaded.
            InvalidConfiguration: if the device class is not a subclass of GenericLaser.
        """
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load the laser class {device_str}."
            ) from exc

        if not issubclass(self.device, GenericLaser):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclasse of qosst_hal.laser.GenericLaser."
            )
        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.parameters = config.get("parameters", self.DEFAULT_PARAMETERS)

    def __str__(self) -> str:
        res = "Alice laser Configuration\n"
        res += "-------------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += f"Parameters : {self.parameters}\n"
        res += "\n"
        return res


class AlicePolarisationRecoveryConfiguration(BaseConfiguration):
    """
    Configuration for automatic polarisation recovery.
    """

    signal_frequency: float  #: Frequency of the signal to send to Bob.
    signal_amplitude: float  #: Amplitude of the signal to send to Bob.

    DEFAULT_SIGNAL_FREQUENCY: float = 20e6  #: Default value of 20MHz for the frequency.
    DEFAULT_SIGNAL_AMPLITUDE: float = 1.0  #: Default value for the amplitude.

    def from_dict(self, config: Dict) -> None:
        """
        Load data from a dict.

        Args:
            config (Dict): dict corresponding to the alice.polarisation_recovery section.
        """
        self.signal_frequency = config.get(
            "signal_frequency", self.DEFAULT_SIGNAL_FREQUENCY
        )
        self.signal_amplitude = config.get(
            "signal_amplitude", self.DEFAULT_SIGNAL_AMPLITUDE
        )

    def __str__(self) -> str:
        res = "Alice Polarisation Recovery Configuration\n"
        res += "-----------------------------------------\n"
        res += f"Signal frequency : {self.signal_frequency*1e-6} MHz"
        res += f"Signal amplitude : {self.signal_amplitude}"
        return res


class AliceConfiguration(BaseConfiguration):
    """
    Complete Alice configuration. It should be initialized with the alice section.
    """

    photodiode_to_output_conversion: (
        float  #: Ratio of conversion from the monitoring photodiode to Alice's output.
    )
    emission_wavelength: (
        float  #: Wavelength of emission used in the measurement of <n>.
    )
    artificial_excess_noise: float  #: Artificial excess noise to add to the generatred signal but not save symbols.
    schema: EmissionSchema  #: Schema of emission.
    network: AliceNetworkConfiguration  #: Network configuration object
    dac: AliceDACConfiguration  #: DAC configuration object
    signal_generation: (
        AliceSignalGenerationConfiguration  #: Signal generation configuration object
    )
    powermeter: AlicePowerMeterConfiguration  #: PowerMeter configuration object
    voa: AliceVOAConfiguration  #: VOA configuration object.
    modulator_bias_control: (
        AliceModulatorBiasControlConfiguration  #: Bias controller configuration object.
    )
    laser: AliceLaserConfiguration  #: Laser configuration object.
    polarisation_recovery: (
        AlicePolarisationRecoveryConfiguration  #: Polarisation recovery configuration.
    )

    DEFAULT_PHOTODIODE_TO_OUTPUT_CONVERSION: float = (
        1  #: Default value for the conversion factor.
    )
    DEFAULT_EMISSION_WAVELENGTH: float = (
        1550e-9  #: Default value for the emission wavelength.
    )
    DEFAULT_ARTIFICIAL_EXCESS_NOISE = (
        0  #: Default value for the artificial excess noise.
    )
    DEFAULT_EMISSION_SCHEMA_STR = (
        "qosst_core.schema.emission.SINGLE_POLARISATION_SINGLE_SIDEBAND"
    )

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict

        Args:
            config (dict): dict corresponding to the alice section

        Raises:
            InvalidConfiguration: if the emission schema cannot be loaded.
            InvalidConfiguration: if the emission schema is not an instance of :class:`qosst_core.schema.emission.EmissionSchema`.
        """
        if "network" not in config:
            logger.warning(
                "alice.network is missing from the configuration file. Using default values for all the parameters."
            )

        if "dac" not in config:
            logger.warning(
                "alice.dac is missing from the configuration file. Using default values for all the parameters."
            )

        if "signal_generation" not in config:
            logger.warning(
                "alice.signal_generation is missing from the configuration file. Using default values for all the parameters."
            )

        if "powermeter" not in config:
            logger.warning(
                "alice.powermeter is missing from the configuration file. Using default values for all the parameters."
            )

        if "voa" not in config:
            logger.warning(
                "alice.voa is missing from the configuration file. Using default values for all the parameters."
            )

        if "modulator_bias_control" not in config:
            logger.warning(
                "alice.modulator_bias_control is missing from the configuration file. Using default values for all the parameters."
            )

        if "laser" not in config:
            logger.warning(
                "alice.laser is missing from the configuration file. Using default values for all the parameters."
            )

        if "polarisation_recovery" not in config:
            logger.warning(
                "alice.polarisation_recovery is missing from the configuration file. Using default values for all the parameters."
            )

        self.photodiode_to_output_conversion = config.get(
            "photodiode_to_output_conversion",
            self.DEFAULT_PHOTODIODE_TO_OUTPUT_CONVERSION,
        )
        self.emission_wavelength = config.get(
            "emission_wavelength", self.DEFAULT_EMISSION_WAVELENGTH
        )
        self.artificial_excess_noise = config.get(
            "artificial_excess_noise", self.DEFAULT_ARTIFICIAL_EXCESS_NOISE
        )

        schema_str = config.get("schema", self.DEFAULT_EMISSION_SCHEMA_STR)
        if schema_str in (
            "qosst_core.schema.emission.SINGLE_POLARISATION",
            "qosst_core.schema.emission.DOUBLE_POLARISATION",
        ):
            warn(
                "qosst_core.schema.emission.SINGLE_POLARISATION and qosst_core.schema.emission.DOUBLE_POLARISATION are depecrated and will be removed in future release of QOSST. Consider replacing them with qosst_core.schema.emission.DOUBLE_POLARISATION_SINGLE_SIDEBAND and qosst_core.schema.emission.DOUBLE_POLARISATION_SINGLE_SIDEBAND",
                FutureWarning,
            )
        try:
            self.schema = get_object_by_import_path(schema_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Impossible to load the detection shema {schema_str}.",
            ) from exc

        if not isinstance(self.schema, EmissionSchema):
            raise InvalidConfiguration(
                f"The emission schema {schema_str} is not an instance of qosst_core.schema.emission.EmissionSchema."
            )

        self.network = AliceNetworkConfiguration(config.get("network", {}))
        self.dac = AliceDACConfiguration(config.get("dac", {}))
        self.signal_generation = AliceSignalGenerationConfiguration(
            config.get("signal_generation", {})
        )
        self.powermeter = AlicePowerMeterConfiguration(config.get("powermeter", {}))
        self.voa = AliceVOAConfiguration(config.get("voa", {}))
        self.modulator_bias_control = AliceModulatorBiasControlConfiguration(
            config.get("modulator_bias_control", {})
        )
        self.laser = AliceLaserConfiguration(config.get("laser", {}))
        self.polarisation_recovery = AlicePolarisationRecoveryConfiguration(
            config.get("polarisation_recovery", {})
        )

    def __str__(self) -> str:
        res = "=========================\n"
        res += "== Alice Configuration ==\n"
        res += "=========================\n"
        res += f"Schema : {str(self.schema)}\n"
        res += f"Photodiode to output conversion : {self.photodiode_to_output_conversion}\n"
        res += f"Emission wavelength: {self.emission_wavelength}\n"
        res += f"Artificial excess noise : {self.artificial_excess_noise}\n"
        res += "\n"
        res += str(self.signal_generation)
        res += str(self.network)
        res += str(self.dac)
        res += str(self.powermeter)
        res += str(self.voa)
        res += str(self.modulator_bias_control)
        res += str(self.laser)
        return res
