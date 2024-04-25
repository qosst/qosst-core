# qosst-core - Core module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2024 Yoann Piétri
# Copyright (C) 2021-2024 Ilektra Karakosta-Amarantidou

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
Configuration for Bob section.
"""
from typing import Type, Any, List, Tuple, Dict
import logging

from qosst_hal.adc import GenericADC
from qosst_hal.switch import GenericSwitch
from qosst_hal.laser import GenericLaser
from qosst_hal.polarisation_controller import GenericPolarisationController
from qosst_hal.powermeter import GenericPowerMeter

from qosst_core.control_protocol import DEFAULT_PORT
from qosst_core.configuration.exceptions import (
    InvalidTime,
    InvalidEta,
    InvalidConfiguration,
)
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.utils import get_object_by_import_path
from qosst_core.skr_computations import BaseCVQKDSKRCalculator
from qosst_core.parameters_estimation import BaseEstimator
from qosst_core.schema.detection import DetectionSchema

logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class BobNetworkConfiguration(BaseConfiguration):
    """
    Class holding the configuration for Bob network. It should correspond to bob.network section.
    """

    server_address: str  #: Address to use for Bob
    server_port: int  #: Port to use for Bob

    DEFAULT_SERVER_ADDRESS: str = "127.0.0.1"  #: Default value for address
    DEFAULT_SERVER_PORT: int = DEFAULT_PORT  #: Default value for port

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict.

        Args:
            config (dict): dict correspoding to the bob.network section.
        """
        self.server_address = config.get("server_address", self.DEFAULT_SERVER_ADDRESS)
        self.server_port = config.get("server_port", self.DEFAULT_SERVER_PORT)

    def __str__(self) -> str:
        res = "Bob Network Configuration\n"
        res += "-------------------------\n"
        res += f"Server address : {self.server_address}\n"
        res += f"Server port : {self.server_port}\n"
        res += "\n"
        return res


class BobADCConfiguration(BaseConfiguration):
    """
    Class holding Bob ADC configuration. It should correspond to the bob.adc section.
    """

    rate: float  #: ADC rate
    device: Type[GenericADC]  #: ADC device to use
    channels: list  #: List of channels to use.
    location: Any  #: Location of the device to use.
    acquisition_time: float  #: Acquisition time, in seconds. If 0 the acquisition time should be computed automatically.
    overhead_time: float  #: Overhead time, in seconds, to compute the acquisition time.
    extra_args: dict  #: Extra args to pass to the ADC class
    extra_acquisition_parameters: (
        dict  #: Extra args to pass to the set_acquisition_parameters method
    )

    DEFAULT_RATE: float = 2500e6  #: Default ADC rate.
    DEFAULT_DEVICE_STR: str = (
        "qosst_hal.adc.FakeADC"  #: Default value for the ADC device.
    )
    DEFAULT_CHANNELS: list = [0]  #: Default list of channels to use.
    DEFAULT_LOCATION: str = ""  #: Default location.
    DEFAULT_ACQUISITION_TIME: float = (
        0  #: Default value for the acquisition time, in seconds.
    )
    DEFAULT_OVERHEAD_TIME: float = (
        0  #: Default value for the overhead time, in seconds.
    )
    DEFAULT_EXTRA_ARGS: dict = {}  #: Default extra args for the ADC.
    DEFAULT_EXTRA_ACQUISITION_PARAMETERS: dict = (
        {}
    )  #: Default extra acquisition parameters.

    def from_dict(self, config: dict) -> None:
        """Fill instance from a dict.

        Args:
            config (dict): dict correspoding to the bob.adc section

        Raises:
            InvalidConfiguration: If the ADC class cannot be loaded.
            InvalidConfiguration: If the ADC class is not a subclass of :class:`~qosst_hal.adc.GenericADC`.
            InvalidTime: if the acquisition time is not valid (strictly below 0).
            InvalidTime: if the overhead time is not valid (strictly below 0).
        """
        self.rate = config.get("rate", self.DEFAULT_RATE)
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(f"Cannot load ADC class {device_str}.") from exc

        if not issubclass(self.device, GenericADC):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclass of qosst_hal.adc.GenericADC."
            )
        self.channels = config.get("channels", self.DEFAULT_CHANNELS)
        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.acquisition_time = config.get(
            "acquisition_time", self.DEFAULT_ACQUISITION_TIME
        )
        if not self.acquisition_time >= 0:
            raise InvalidTime(self.acquisition_time)

        self.overhead_time = config.get("overhead_time", self.DEFAULT_OVERHEAD_TIME)
        if not self.overhead_time >= 0:
            raise InvalidTime(self.overhead_time)

        self.extra_args = config.get("extra_args", self.DEFAULT_EXTRA_ARGS)
        self.extra_acquisition_parameters = config.get(
            "extra_acquisition_parameters", self.DEFAULT_EXTRA_ACQUISITION_PARAMETERS
        )

    def __str__(self) -> str:
        res = "Bob ADC Configuration\n"
        res += "---------------------\n"
        res += f"Rate : {self.rate*1e-6} MSamples/s\n"
        res += f"Device : {self.device}\n"
        res += f"Channels : {self.channels}\n"
        res += f"Location : {self.location}\n"
        res += f"Acquisition time : {self.acquisition_time} s\n"
        res += f"Extra args : {self.extra_args}\n"
        res += f"Extra acquisition parameters : {self.extra_acquisition_parameters}\n"
        res += "\n"
        return res


class BobSwitchConfiguration(BaseConfiguration):
    """
    Class holding switch configuration for Bob. It should correspond to the bob.switch section.
    """

    device: Type[GenericSwitch]  #: Device for the switch.
    location: str  #: Location of the switch.
    timeout: int  #: Timeout in seconds.
    signal_state: int  #: State for the signal.
    calibration_state: int  #: State for the calibration.
    switching_time: float  #: Time to wait before switching to the signal state. If 0, not automatic switching is done.

    DEFAULT_DEVICE_STR: str = "FakeSwitch"  #: Default device for the switch.
    DEFAULT_LOCATION: str = ""  #: Default location for the switch.
    DEFAULT_TIMEOUT: int = 100  #: Default timeout for the switch.
    DEFAULT_SIGNAL_STATE: int = 1  #: Default signal state for the switch.
    DEFAULT_CALIBRATION_STATE: int = 2  #: Default calibration state for the switch.
    DEFAULT_SWITCHING_TIME: float = 0  #: Default value for the switching time.

    def from_dict(self, config: dict):
        """Read configuration from dict.

        Args:
            config (dict): dict holding the switch part of Bob's configuration.

        Raises:
            InvalidConfiguration: if the device class cannot be loaded.
            InvalidConfiguration: if the device class is found but is not a subclass of :class:`~qosst_hal.switch.GenericSwitch`.
        """
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load switch class {device_str}."
            ) from exc

        if not issubclass(self.device, GenericSwitch):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclass of qosst_hal.switch.GenericSwitch."
            )

        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.timeout = config.get("timeout", self.DEFAULT_TIMEOUT)
        self.signal_state = config.get("signal_state", self.DEFAULT_SIGNAL_STATE)
        self.calibration_state = config.get(
            "calibration_state", self.DEFAULT_CALIBRATION_STATE
        )
        self.switching_time = config.get("switching_time", self.DEFAULT_SWITCHING_TIME)

    def __str__(self) -> str:
        res = "Bob Switch Configuration\n"
        res += "------------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += f"Timeout : {self.location}\n"
        res += f"Signal state : {self.signal_state}\n"
        res += f"Calibration state : {self.calibration_state}\n"
        res += f"Switching time : {self.switching_time}\n"
        res += "\n"
        return res


class BobPolarisationRecoveryPolarisationControllerConfiguration(BaseConfiguration):
    """
    Class holding the configuration for the motorized polarisation controller device
    for automatic polarisation recovery.
    """

    device: Type[
        GenericPolarisationController
    ]  #: Class of the polarisation controller to use.
    location: str  #: Location of the device.

    DEFAULT_DEVICE_STR: str = (
        "qosst_hal.polarisation_controller.FakePolarisationController"  #: Default device for the polarisation controller.
    )
    DEFAULT_LOCATION: str = ""  #: Default location for the polarisation controller.

    def from_dict(self, config: Dict) -> None:
        """
        Read the configuration from dict. The dict should correspond to the
        bob.polarisation_recovery.polarisation_controller section.

        Args:
            config (Dict): dict corresponding to the bob.polarisation_recovery.polarisation_controller section.

        Raises:
            InvalidConfiguration: if the class for the device cannot be loaded.
            InvalidConfiguration: if the class for the device is not a subclass of qosst_hal.polarisation_controller.GenericPolarisationController.
        """
        device_str = config.get("device", self.DEFAULT_DEVICE_STR)
        try:
            self.device = get_object_by_import_path(device_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load polarisation controller class {device_str}."
            ) from exc

        if not issubclass(self.device, GenericPolarisationController):
            raise InvalidConfiguration(
                f"The device {device_str} is not a subclass of qosst_hal.polarisation_controller.GenericPolarisationController."
            )

        self.location = config.get("location", self.DEFAULT_LOCATION)

    def __str__(self) -> str:
        res = "Bob Polarisation Controller Configuration\n"
        res += "-----------------------------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += "\n"
        return res


class BobPolarisationRecoveryPowermeterConfiguration(BaseConfiguration):
    """
    Configuration for the powermeter for the polarisation recovery.
    """

    device: Type[
        GenericPowerMeter
    ]  #: Class of device to use for the powermeter for polarisation recovery.
    location: str  #: Location of the powermeter for polarisation recovery.
    timeout: int  #: Timeout for the powermeter.

    DEFAULT_DEVICE_STR: str = (
        "qosst_hal.powermeter.FakePowerMeter"  #: Default value for the powermeter device.
    )
    DEFAULT_LOCATION: str = ""
    DEFAULT_TIMEOUT: int = 10

    def from_dict(self, config: Dict) -> None:
        """
        Load the data from dict.

        Args:
            config (Dict): dict corresponding ot the bob.polarisation_recovery.powermeter section.
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
                f"The device {device_str} is not a subclass of qosst_hal.powetermeter.GenericPowerMeter"
            )

        self.location = config.get("location", self.DEFAULT_LOCATION)
        self.timeout = config.get("timeout", self.DEFAULT_TIMEOUT)

    def __str__(self) -> str:
        res = "Bob Powermeter Configuration\n"
        res += "----------------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += "\n"
        return res


class BobPolarisationRecoveryConfiguration(BaseConfiguration):
    """
    Configuration for the automatic polarisation recovery.
    """

    use: bool  #: If true, use the automatic polarisation recovery.
    step: float  #: Step of the polarisation recovery algorithm (unit depends on polarisation controller).
    start_course: float  #: Value of the first position to test.
    end_course: float  #: Value of the last position to test (excluded).
    wait_time: float  #: Wait time, in seconds, between two positions.
    polarisation_controller: BobPolarisationRecoveryPolarisationControllerConfiguration  #: Configuration for the polarisation controller.
    powermeter: BobPolarisationRecoveryPowermeterConfiguration  #: Configuration for the powermeter

    DEFAULT_USE: bool = False  #: Default value for use.
    DEFAULT_STEP: float = 1.0  #: Default value for the step.
    DEFAULT_START_COURSE: float = 0.0  #: Default value for the start course.
    DEFAULT_END_COURSE: float = 0.0  #: Default value for the end course.
    DEFAULT_WAIT_TIME: float = 0.0  #: Default value for the wait time.

    def from_dict(self, config: Dict) -> None:
        """
        Load the data from dict.

        Args:
            config (Dict): dict corresponding ot the bob.polarisation_recovery section.
        """
        self.use = config.get("use", self.DEFAULT_USE)
        self.step = config.get("step", self.DEFAULT_STEP)
        self.start_course = config.get("start_course", self.DEFAULT_START_COURSE)
        self.end_course = config.get("end_course", self.DEFAULT_END_COURSE)
        self.wait_time = config.get("wait_time", self.DEFAULT_WAIT_TIME)
        self.polarisation_controller = (
            BobPolarisationRecoveryPolarisationControllerConfiguration(
                config.get("polarisation_controller", {})
            )
        )
        self.powermeter = BobPolarisationRecoveryPowermeterConfiguration(
            config.get("powermeter", {})
        )

    def __str__(self) -> str:
        res = "Bob Polarisation Controller Configuration\n"
        res += "-----------------------------------------\n"
        res += f"Use : {self.use}\n"
        res += f"Step : {self.step}\n"
        res += f"Start course : {self.start_course}\n"
        res += f"End course : {self.end_course}\n"
        res += f"Wait time : {self.wait_time}"
        res += "\n"
        res += str(self.polarisation_controller)
        res += str(self.powermeter)
        return res


class BobDSPEqualizerConfiguration(BaseConfiguration):
    """
    Class holding the DSP CMA equalizer configuration for Bob. It should correspond to the bob.dsp.equalizer section.
    """

    equalize: bool  # If true, use the CMA equalizer.
    length: int  # Length of the CMA equalizer.
    step: float  # Step size for the CMA equalizer.
    p_param: int  # P-parameter of the CMA equalizer.
    q_param: int  # Q-parameter of the CMA equalizer.

    DEFAULT_EQUALIZE: bool = False  #: Default value for the use of equalization
    DEFAULT_LENGTH: int = 100  # Default value for the length of the equalizer
    DEFAULT_STEP: float = 0.01  # Default value for the step of the equalizer
    DEFAUL_P_PARAM: int = 2  # Default value for the p-parameter of the CMA equalizer
    DEFAULT_Q_PARAM: int = 2  # Default value for the p-parameter of the CMA equalizer

    def from_dict(self, config: dict) -> None:
        """Read configuration from dict.

        Args:
            config (dict): dict holding the equalizer part of Bob's DSP configuration.
        """
        self.equalize = config.get("equalize", self.DEFAULT_EQUALIZE)
        self.length = config.get("length", self.DEFAULT_LENGTH)
        self.step = config.get("step", self.DEFAULT_STEP)
        self.p_param = config.get("p", self.DEFAUL_P_PARAM)
        self.q_param = config.get("q", self.DEFAULT_Q_PARAM)

    def __str__(self) -> str:
        res = "Bob DSP Equalizer Configuration\n"
        res += "-------------------------------\n"
        res += f"Enable equalization : {self.equalize}\n"
        res += f"Equalizer length : {self.length}\n"
        res += f"Equalizer step size : {self.step}\n"
        res += f"Equalizer p-parameter : {self.p_param}\n"
        res += f"Equalizer q-parameter : {self.q_param}\n"
        res += "\n"
        return res


class BobDSPConfiguration(BaseConfiguration):
    """
    Class holding DSP configuration for Bob. It should correspond to the bob.dsp section.
    """

    debug: bool  #: Debug mode.
    fir_size: int
    tone_filtering_cutoff: (
        float  #: Cutoff for the FIR filter for the filtering of the pilot tone.
    )
    process_subframes: bool
    subframes_size: int
    abort_clock_recovery: float  #: Maximal value of clock mismatch allowed to be found by clock recovery algorithm.
    alice_dac_rate: float  #: DAC rate of Alice
    exclusion_zone_pilots: List[
        Tuple[float, float]
    ]  # List of exclusion zones for the pilot search.
    pilot_phase_filtering_size: int  #: Size of uniform1d filter for the phase recovery.
    num_samples_fbeat_estimation: (
        int  #: Number of samples to estimate f_beat in general DSP.
    )
    equalizer: (
        BobDSPEqualizerConfiguration  #: The equalizer part of Bob's DSP configuration
    )

    DEFAULT_DEBUG: bool = True  #: Default value fot the debug mode.
    DEFAULT_FIR_SIZE: int = 500
    DEFAULT_TONE_FILTERING_CUTOFF: float = (
        10e6  #: Default value for the cutoff of the FIR filter for the filtering of the tone.
    )
    DEFAULT_PROCESS_SUBFRAMES: bool = False
    DEFAULT_SUBFRAMES_SIZE: int = 0
    DEFAULT_ABORT_CLOCK_RECOVERY: float = 0  #: Default value for abort_clock_recovery.
    DEFAULT_ALICE_DAC_RATE: float = 500e6  #: Default value for the DAC rate of Alice.
    DEFAULT_EXCLUSION_ZONE_PILOTS: List[List[float]] = [
        [0.0, 100e3]
    ]  #: Default value for the exclusion zone for the search of the pilots.
    DEFAULT_PILOT_PHASE_FILTERING_SIZE: int = (
        0  #: Default value for the filtering size of the phase for the phase recovery.
    )
    DEFAULT_NUM_SAMPLES_FBEAT_ESTIMATION: int = 100000

    def from_dict(self, config: dict) -> None:
        """Read configuration from dict.

        Args:
            config (dict): dict holding the DSP part of Bob's configuration.
        """
        if not "equalizer" in config:
            logger.warning(
                "bob.dsp.equalizer is missing from the configuration file. Using default values for all the parameters."
            )

        self.debug = config.get("debug", self.DEFAULT_DEBUG)
        self.fir_size = config.get("fir_size", self.DEFAULT_FIR_SIZE)
        self.tone_filtering_cutoff = config.get(
            "tone_filtering_cutoff", self.DEFAULT_TONE_FILTERING_CUTOFF
        )
        self.process_subframes = config.get(
            "process_subframes", self.DEFAULT_PROCESS_SUBFRAMES
        )
        self.subframes_size = config.get("subframes_size", self.DEFAULT_SUBFRAMES_SIZE)
        self.abort_clock_recovery = config.get(
            "abort_clock_recovery", self.DEFAULT_ABORT_CLOCK_RECOVERY
        )
        self.alice_dac_rate = config.get("alice_dac_rate", self.DEFAULT_ALICE_DAC_RATE)
        exclusion = config.get(
            "exclusion_zone_pilots", self.DEFAULT_EXCLUSION_ZONE_PILOTS
        )
        self.exclusion_zone_pilots = [(zone[0], zone[1]) for zone in exclusion]
        self.pilot_phase_filtering_size = config.get(
            "pilot_phase_filtering_size", self.DEFAULT_PILOT_PHASE_FILTERING_SIZE
        )
        self.num_samples_fbeat_estimation = config.get(
            "num_samples_fbeat_estimation", self.DEFAULT_NUM_SAMPLES_FBEAT_ESTIMATION
        )
        self.equalizer = BobDSPEqualizerConfiguration(config.get("equalizer", {}))

    def __str__(self) -> str:
        res = "Bob DSP Configuration\n"
        res += "---------------------\n"
        res += f"Debug : {self.debug}\n"
        res += f"FIR size : {self.fir_size}\n"
        res += f"Tone filtering cut-off: {self.tone_filtering_cutoff}\n"
        res += f"Process subframes : {self.process_subframes}\n"
        res += f"Subframes size : {self.subframes_size}\n"
        res += f"Abort clock recovery : {self.abort_clock_recovery}\n"
        res += f"Alice DAC rate : {self.alice_dac_rate}\n"
        res += f"Exclusion zone : {self.exclusion_zone_pilots}\n"
        res += f"Pilot phase filtering size : {self.pilot_phase_filtering_size}\n"
        res += f"Number of samples for fbeat estimation : {self.DEFAULT_NUM_SAMPLES_FBEAT_ESTIMATION}\n"
        res += "\n"
        res += str(self.equalizer)
        return res


class BobParametersEstimation(BaseConfiguration):
    """
    Configuration for parameters estimation of Bob. It should correspond to the bob.parameters_estimation section.
    """

    estimator: Type[BaseEstimator]  #: The class of the estimator.
    skr_calculator: Type[BaseCVQKDSKRCalculator]  #: The class of the SKR calculator.
    ratio: float  #: Ratio of data to use for parameters estimation.

    DEFAULT_ESTIMATOR_STR: str = (
        "qosst_bob.parameters_estimation.DefaultEstimator"  #: Default estimator.
    )
    DEFAULT_SKR_CALCULATOR: str = (
        "qosst_skr.HeterodyneTrustedAsymptoticSKRCalculator"  #: Default skr calculator
    )
    DEFAULT_RATIO: float = (
        0.5  #: Default value for the ratio: 50% is used for parameters estimation.
    )

    def from_dict(self, config: Dict) -> None:
        """Load the configuration from dict.

        Args:
            config (Dict): dict corresponding the bob.parameters_estimation section.

        Raises:
            InvalidConfiguration: if the estimator class cannot be loaded.
            InvalidConfiguration: if the skr class cannot be loaded.
        """
        estimator_str = config.get("estimator", self.DEFAULT_ESTIMATOR_STR)
        try:
            self.estimator = get_object_by_import_path(estimator_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load estimator class {estimator_str}."
            ) from exc

        skr_calculator_str = config.get("skr_calculator", self.DEFAULT_SKR_CALCULATOR)
        try:
            self.skr_calculator = get_object_by_import_path(skr_calculator_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load estimator class {skr_calculator_str}."
            ) from exc

        self.ratio = config.get("ratio", self.DEFAULT_RATIO)

        if not 0 <= self.ratio <= 1:
            raise InvalidConfiguration(
                "The ratio for parameters estimation should be a float between 0 and 1 (0% and 100%)."
            )

    def __str__(self):
        res = "Bob Parameters Estimation Configuration\n"
        res += "---------------------------------------\n"
        res += f"Estimator : {self.estimator}\n"
        res += f"SKR calculator : {self.skr_calculator}\n"
        res += f"Ratio : {self.ratio}"
        res += "\n"
        return res


class BobLaserConfiguration(BaseConfiguration):
    """
    Configuration for Bob's laser section. It should correspond to the bob.laser section.
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
            config (dict): dict corresponding to the bob.laser section.

        Raises:
            Exception: if the device class cannot be loaded.
            Exception: if the device class is not a subclass of qosst_hal.laser.GenericLaser.
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
        res = "Bob laser Configuration\n"
        res += "-------------------------\n"
        res += f"Device : {self.device}\n"
        res += f"Location : {self.location}\n"
        res += f"Parameters : {self.parameters}\n"
        res += "\n"
        return res


class BobElectronicNoiseConfiguration(BaseConfiguration):
    """
    Class holding the configuration of the bob.electronic_noise section.
    """

    path: str  #: Path to load and save the electronic noise.

    DEFAULT_PATH: str = "electronic_noise.qosst"  #: Default path.

    def from_dict(self, config: dict) -> None:
        """Fill the configuration from a dict.

        Args:
            config (dict): dict corresponding to the bob.electronic_noise section.
        """
        self.path = config.get("path", self.DEFAULT_PATH)

    def __str__(self) -> str:
        res = "Bob electronic noise configuration\n"
        res += "----------------------------------\n"
        res += f"Path : {self.path}\n"
        res += "\n"
        return res


class BobElectronicShotNoiseConfiguration(BaseConfiguration):
    """
    Class holding the configuration of the bob.electronic_shot_noise section.
    """

    path: str  #: Path to load and save the electronic and shot noise.

    DEFAULT_PATH: str = "electronic_shot_noise.qosst"  #: Default path.

    def from_dict(self, config: dict) -> None:
        """Fill the configuration from a dict.

        Args:
            config (dict): dict corresponding to the bob.electronic_shot_noise section.
        """
        self.path = config.get("path", self.DEFAULT_PATH)

    def __str__(self) -> str:
        res = "Bob electronic and shot noise configuration\n"
        res += "-------------------------------------------\n"
        res += f"Path : {self.path}\n"
        res += "\n"
        return res


# pylint: disable=too-many-instance-attributes
class BobConfiguration(BaseConfiguration):
    """
    Class holding Bob configuration. It should correspond to the bob section.
    """

    export_directory: str  #: Path of directory where to export the data
    eta: float  #: Global efficiency of the detector. Must be between 0 and 1.
    automatic_shot_noise_calibration: bool  #: If true, shot nosie calibration is performed automatically before trigger.
    schema: DetectionSchema  #: Schema of detection.
    network: BobNetworkConfiguration  #: The netwokr configuration of Bob
    adc: BobADCConfiguration  #: The ADC configuration of Bob
    switch: BobSwitchConfiguration  #: The switch configuration
    dsp: BobDSPConfiguration  #: The DSP configuration
    parameters_estimation: (
        BobParametersEstimation  #: The parameters estimation configuration.
    )
    laser: BobLaserConfiguration  #: The laser configuration.
    polarisation_recovery: BobPolarisationRecoveryConfiguration  #: The polarisation recovery configuration.
    electronic_noise: (
        BobElectronicNoiseConfiguration  #: The electronic noise configuration.
    )
    electronic_shot_noise: BobElectronicShotNoiseConfiguration  #: The electronic and shot noise configuration.

    DEFAULT_EXPORT_DIRECTORY: str = "export"  #: Default value for the export path
    DEFAULT_ETA: float = 0.8  #: Default value for eta
    DEFAULT_AUTOMATIC_SHOT_NOISE_CALIBRATION: bool = (
        False  #: Default value for the automatic shot noise calibration.
    )
    DEFAULT_DETECTION_SCHEMA_STR: str = (
        "qosst_core.schema.detection.SINGLE_POLARISATION_RF_HETERODYNE"  #: Default detection schema.
    )

    def from_dict(self, config: dict) -> None:
        """Fill instance from the config.

        Args:
            config (dict): dict corresponding to the bob section.

        Raises:
            InvalidEta: if eta is not between 0 and 1.
            InvalidConfiguration: if the detection schema cannot be loaded.
            InvalidConfiguration: if the detection schema is not an instance of :class:`qosst_core.schema.detection.DetectionSchema`.
        """
        if "network" not in config:
            logger.warning(
                "bob.network is missing from the configuration file. Using default values for all the parameters."
            )

        if "adc" not in config:
            logger.warning(
                "bob.adc is missing from the configuration file. Using default values for all the parameters."
            )

        if "switch" not in config:
            logger.warning(
                "bob.switch is missing from the configuration file. Using default values for all the parameters."
            )

        if "dsp" not in config:
            logger.warning(
                "bob.dsp is missing from the configuration file. Using default values for all the parameters."
            )

        if "parameters_estimation" not in config:
            logger.warning(
                "bob.parameters_estimation is missing from the configuration file. Using default values for all the parameters."
            )

        if "laser" not in config:
            logger.warning(
                "bob.laser is missing from the configuration file. Using default values for all the parameters."
            )

        if not "polarisation_revovery" in config:
            logger.warning(
                "bob.polarisation_recovery is missing from the configuration file. Using default values for all the parameters."
            )

        if "electronic_noise" not in config:
            logger.warning(
                "bob.electronic_noise is missing from the configuration file. Using default values for all the parameters."
            )

        if "electronic_shot_noise" not in config:
            logger.warning(
                "bob.electronic_shot_noise is missing from the configuration file. Using default values for all the parameters."
            )

        self.export_directory = config.get(
            "export_directory", self.DEFAULT_EXPORT_DIRECTORY
        )
        self.eta = config.get("eta", self.DEFAULT_ETA)
        if not 0 <= self.eta <= 1:
            raise InvalidEta(self.eta)
        self.automatic_shot_noise_calibration = config.get(
            "automatic_shot_noise_calibration",
            self.DEFAULT_AUTOMATIC_SHOT_NOISE_CALIBRATION,
        )
        schema_str = config.get("schema", self.DEFAULT_DETECTION_SCHEMA_STR)
        try:
            self.schema = get_object_by_import_path(schema_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Impossible to load the detection shema {schema_str}.",
            ) from exc

        if not isinstance(self.schema, DetectionSchema):
            raise InvalidConfiguration(
                f"The detection schema {schema_str} is not an instance of qosst_core.schema.detection.DetectionSchema."
            )

        self.network = BobNetworkConfiguration(config.get("network", {}))
        self.adc = BobADCConfiguration(config.get("adc", {}))
        self.switch = BobSwitchConfiguration(config.get("switch", {}))
        self.dsp = BobDSPConfiguration(config.get("dsp", {}))
        self.parameters_estimation = BobParametersEstimation(
            config.get("parameters_estimation", {})
        )
        self.laser = BobLaserConfiguration(config.get("laser", {}))
        self.polarisation_recovery = BobPolarisationRecoveryConfiguration(
            config.get("polarisation_recovery", {})
        )
        self.electronic_noise = BobElectronicNoiseConfiguration(
            config.get("electronic_noise", {})
        )
        self.electronic_shot_noise = BobElectronicShotNoiseConfiguration(
            config.get("electronic_shot_noise", {})
        )

    def __str__(self) -> str:
        res = "=======================\n"
        res += "== Bob Configuration ==\n"
        res += "=======================\n"
        res += f"Schema : {str(self.schema)}\n"
        res += f"Export directory : {self.export_directory}\n"
        res += f"η (eta) : {self.eta}\n"
        res += f"Automatic shot noise calibration : {self.automatic_shot_noise_calibration}\n"
        res += "\n"
        res += str(self.network)
        res += str(self.adc)
        res += str(self.switch)
        res += str(self.dsp)
        res += str(self.parameters_estimation)
        res += str(self.laser)
        res += str(self.electronic_noise)
        res += str(self.electronic_shot_noise)
        return res
