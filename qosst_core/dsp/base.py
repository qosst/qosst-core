# qosst-core - Core module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2026 Yoann Piétri

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
Generic class for class-based DSP.
"""

import abc
import logging
from typing import Optional, List, Tuple, Type, Dict, Any

import numpy as np

from qosst_core.configuration import Configuration
from qosst_core.synchronization import BaseSynchronizationSequence
from qosst_core.dsp.phase_estimator import BasePhaseEstimator
from qosst_core.dsp.timing_estimator import BaseTimingRecoveryEstimator
from qosst_core.schema.detection import (
    DetectionSchema,
    SINGLE_POLARISATION_RF_HETERODYNE,
)

logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class BaseDSP(abc.ABC):
    """Base DSP class."""

    unsafe: bool = False  #: True if the DSP was not tested with the latest hardware.

    debug_object: Optional[
        Dict[str, Any]
    ]  #: Debug object returned when calling get_debug.
    parameters_set: bool = False  #: Test if the parameters have been set.
    special_parameters_set: bool = (
        False  #: Test of the special parameters have been set.
    )

    # DSP parameters
    symbol_rate: float  #: Symbol rate in Baud.
    dac_rate: float  #: DAC rate in Sample/s.
    adc_rate: float  #: ADC rate in Sample/s.
    num_symbols: int  #: Number of symbols to recover.
    roll_off: float  #: Roll off factor the root-raised cosine filter.
    frequency_shift: float  #: Expected frequency shift of the quantum data in Hz.
    num_pilots: int  #: Number of expected pilots.
    pilots_frequencies: np.ndarray[
        float
    ]  #: Array of expected frequencies of the pilots.
    synchronization_cls: Type[
        BaseSynchronizationSequence
    ]  #: Type of synchronization sequence.
    zc_length: int  #: Length of the Zadoff-Chu sequence (ZC sequence only).
    zc_root: int  #: Root of the Zadoff-Chu sequence (ZC sequence only).
    mls_nbits: (
        int  #: Number of bits for the maximum length sequence (MLS sequence only).
    )
    synchro_rate: float  #: Rate of the synchronization sequence in Sample/s.
    phase_estimator_cls: Type[
        BasePhaseEstimator
    ]  #: Type of phase estimator algorithm to use.
    timing_estimator_cls: Type[
        BaseTimingRecoveryEstimator
    ]  #: Type of timing recovery algorithm to use.
    switching_time: (
        float  #: Switching time in seconds when using automatic shot noise recovery.
    )
    linewidth: float  #: Linewidth in Hz for the phase estimator.
    subframe_length: int  #: Subframe length when performing the DSP iun subframes.
    subframe_subdivision: (
        int  #: Subdivision of a subframe for a finer-grained global phase recovery.
    )
    fir_size: int  #: Size of the finite impulse response filter.
    tone_filtering_cutoff: float  #: Cutoff value in Hz when filtering the pilot.
    abort_clock_recovery: float  #: Maximal clock offset before aborting clock recovery.
    pilots_exclusion_zones: Optional[
        List[Tuple[float, float]]
    ]  #: Exclusion zones when searching for the pilots.
    pilot_phase_filtering_size: (
        int  #: Rolling average filter size for the pilots (phase).
    )
    pilot_frequency_filtering_size: (
        int  #: Rolling average filter size for the pilots (frequency).
    )
    symbol_timing_oversampling: int  #: Factor by which the signal is oversampled when searching for the optimal symbol sampling time
    num_samples_fbeat_estimation: (
        float  #: Number of samples for estimating the beat frequency.
    )
    num_samples_pilot_search: (
        int  #: number of samples for estimating the frequency of pilots.
    )
    schema: DetectionSchema  #: Detection schema.
    debug: bool = True  #: Debug mode of the DSP.

    # Special DSP parameters
    elec_noise_estimation_ratio: (
        float  #: Ratio for downsampling electronic noise samples for special DSP.
    )
    elec_shot_noise_estimation_ratio: float  #: Ratio for downsampling electronic and shot noise samples for special DSP.

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
    def set_parameters(
        self,
        symbol_rate: float,
        dac_rate: float,
        adc_rate: float,
        num_symbols: int,
        roll_off: float,
        frequency_shift: float,
        num_pilots: int,
        pilots_frequencies: np.ndarray,
        synchronization_cls: Type[BaseSynchronizationSequence],
        zc_length: int,
        zc_root: int,
        mls_nbits: int,
        synchro_rate: float,
        phase_estimator_cls: Type[BasePhaseEstimator],
        timing_estimator_cls: Type[BaseTimingRecoveryEstimator],
        switching_time: float = 0.02,
        linewidth: float = 5e3,
        subframe_length: int = 50_000,
        subframe_subdivision: int = 1,
        fir_size: int = 500,
        tone_filtering_cutoff: float = 10e6,
        abort_clock_recovery: float = 0,
        pilots_exclusion_zones: Optional[List[Tuple[float, float]]] = None,
        pilot_phase_filtering_size: int = 0,
        pilot_frequency_filtering_size: int = 0,
        symbol_timing_oversampling: int = 1,
        num_samples_fbeat_estimation: int = 100_000,
        num_samples_pilot_search: int = 1_000_000,
        schema: DetectionSchema = SINGLE_POLARISATION_RF_HETERODYNE,
        debug: bool = False,
        elec_noise_estimation_ratio: float = 1.0,
        elec_shot_noise_estimation_ratio: float = 1.0,
    ):
        """
        Set the parameters of the DSP.

        Args:
            data (np.ndarray): data measured by Bob.
            symbol_rate (float): symbol rate in symbols per second.
            dac_rate (float): DAC rate, in Hz.
            adc_rate (float): ADC rate, in Hz.
            num_symbols (int): number of symbols.
            roll_off (float): roll-off factor for the RRC filter.
            frequency_shift (float): frequency shift of the quantum symbol, in Hz.
            num_pilots (int): number of pilots.
            pilots_frequencies (np.ndarray): list of the frequencies of the pilots.
            synchronization_cls (Type[SynchronizationSequence]): class generating the synchronization sequence.
            zc_length (int): length of the Zadoff-Chu sequence.
            zc_root (int): root of the Zadoff-Chu sequence.
            mls_nbits (int): number of bits of the Maximum Length Sequence.
            synchro_rate (float): rate of the synchronization sequence.
            phase_estimator_cls (Type[PhaseEstimator]): class to use for the estimation of the phase of the pilot.
            subframe_length (int, optional): number of symbols to recover in each subframes. Defaults to 50000.
            subframe_subdivision (int, optional): number of subdivisions of each frame for a finer-grained global phase recovery. Defaults to 1.
            fir_size (int, optional): size of the FIR filters. Defaults to 500.
            tone_filtering_cutoff (float, optional): cutoff, in Hz, for the pilot filtering. Defaults to 10e6.
            abort_clock_recovery (float, optional): maximal mismatch allowed by the clock recovery algorithm before aborting. If 0, the algorithm never aborts.. Defaults to 0.
            pilots_exclusion_zones (Optional[List[Tuple[float, float]]], optional): exclusion zones for the research of pilots (i.e. frequencies where we are sure the pilots are not), given as a list of tuples of float, each elements defining excluded segment (start frequency, stop frequency). Defaults to None.
            pilot_phase_filtering_size (int, optional): size of the uniform1d filter to filter the phase correction. Defaults to 0.
            pilot_frequency_filtering_size (int, optional): size of the uniform1d filter to filter the phase correction. Defaults to 0.
            symbol_timing_oversampling (int, optional): by which factor the signal is oversampled when searching for the optimal symbol sampling time. Defaults to 1.
            num_samples_fbeat_estimation (int, optional): number of samples to estimate the beat frequency between the two lasers. Defaults to 100_000.
            num_samples_pilot_search (int, optional): number of samples to estimate the frequency of pilots. Defaults to 10000000.
            schema (DetectionSchema, optional): detection schema to use for the DSP. Defaults to qosst_core.schema.emission.SINGLE_POLARISATION_RF_HETERODYNE.
            debug (bool, optional): if True, the DSPDebug object is returned. Defaults to False.
            elec_noise_estimation_ratio (float, optional): Ratio for downsampling electronic noise samples for special DSP. Defaults to 1.
            elec_shot_noise_estimation_ratio (float, optional): Ratio for downsampling electronic and shot noise samples for special DSP. Defaults to 1.
        """
        self.symbol_rate = symbol_rate
        self.dac_rate = dac_rate
        self.adc_rate = adc_rate
        self.num_symbols = num_symbols
        self.roll_off = roll_off
        self.frequency_shift = frequency_shift
        self.num_pilots = num_pilots
        self.pilots_frequencies = pilots_frequencies
        self.synchronization_cls = synchronization_cls
        self.zc_length = zc_length
        self.zc_root = zc_root
        self.mls_nbits = mls_nbits
        self.synchro_rate = synchro_rate
        self.phase_estimator_cls = phase_estimator_cls
        self.timing_estimator_cls = timing_estimator_cls
        self.switching_time = switching_time
        self.linewidth = linewidth
        self.subframe_length = subframe_length
        self.subframe_subdivision = subframe_subdivision
        self.fir_size = fir_size
        self.tone_filtering_cutoff = tone_filtering_cutoff
        self.abort_clock_recovery = abort_clock_recovery
        self.pilots_exclusion_zones = pilots_exclusion_zones
        self.pilot_phase_filtering_size = pilot_phase_filtering_size
        self.pilot_frequency_filtering_size = pilot_frequency_filtering_size
        self.symbol_timing_oversampling = symbol_timing_oversampling
        self.num_samples_fbeat_estimation = num_samples_fbeat_estimation
        self.num_samples_pilot_search = num_samples_pilot_search
        self.schema = schema
        self.debug = debug
        self.elec_noise_estimation_ratio = elec_noise_estimation_ratio
        self.elec_shot_noise_estimation_ratio = elec_shot_noise_estimation_ratio

        self.parameters_set = True

    def configure_from_config(self, config: Configuration):
        """Configure the DSP from a :class:`~qosst_core.configuration.config.Configuration` object..

        Args:
            config (Configuration): configuration objecs to get parameters from.
        """
        self.set_parameters(
            config.frame.quantum.symbol_rate,
            config.bob.dsp.alice_dac_rate,
            config.bob.adc.rate,
            config.frame.quantum.num_symbols,
            config.frame.quantum.roll_off,
            config.frame.quantum.frequency_shift,
            config.frame.pilots.num_pilots,
            config.frame.pilots.frequencies,
            config.frame.synchronization.synchronization_cls,
            config.frame.synchronization.zc_length,
            config.frame.synchronization.zc_root,
            config.frame.synchronization.mls_nbits,
            config.frame.synchronization.rate,
            config.bob.dsp.phase_estimator,
            config.bob.dsp.timing_recovery_estimator,
            config.bob.switch.switching_time,
            config.bob.dsp.linewidth,
            config.bob.dsp.subframes_size,
            config.bob.dsp.subframes_subdivisions,
            config.bob.dsp.fir_size,
            config.bob.dsp.tone_filtering_cutoff,
            config.bob.dsp.abort_clock_recovery,
            config.bob.dsp.exclusion_zone_pilots,
            config.bob.dsp.pilot_phase_filtering_size,
            config.bob.dsp.pilot_frequency_filtering_size,
            config.bob.dsp.symbol_timing_oversampling,
            config.bob.dsp.num_samples_fbeat_estimation,
            config.bob.dsp.num_samples_pilot_search,
            config.bob.schema,
            config.bob.dsp.debug,
            config.bob.dsp.elec_noise_estimation_ratio,
            config.bob.dsp.elec_shot_noise_estimation_ratio,
        )

    @abc.abstractmethod
    def _run_dsp(
        self,
        data: np.ndarray,
        electronic_noise_data: Optional[List[np.ndarray]] = None,
        electronic_shot_noise_data: Optional[List[np.ndarray]] = None,
    ) -> Optional[List[np.ndarray]]:
        """Actually run the digital signal processing stack.

        Args:
            data (np.ndarray): data to apply the DSP on.
            electronic_noise_data (List[np.ndarray], optional): electronic noise data. Maybe be used by some DSPs. Defaults to None.
            electronic_shot_noise_data (List[np.ndarray], optional): electronic and shot noise data. Maybe be used by some DSPs. Defaults to None.

        Returns:
            Optional[List[np.ndarray]]: recovered symbols.
        """

    def dsp(
        self,
        data: np.ndarray,
        electronic_noise_data: Optional[List[np.ndarray]] = None,
        electronic_shot_noise_data: Optional[List[np.ndarray]] = None,
    ) -> Optional[List[np.ndarray]]:
        """Apply the digital signal processing stack.

        Args:
            data (np.ndarray): data to apply the DSP on.
            electronic_noise_data (List[np.ndarray], optional): electronic noise data. Maybe be used by some DSPs. Defaults to None.
            electronic_shot_noise_data (List[np.ndarray], optional): electronic and shot noise data. Maybe be used by some DSPs. Defaults to None.

        Returns:
            Optional[List[np.ndarray]]: recovered symbols or None.
        """
        if self.unsafe:
            logger.warning("Using untested DSP.")

        if not self.parameters_set:
            logger.critical("Calling the DSP before the parameters are set.")
            return None

        if self.debug:
            logger.info("DSP debug mode is on.")
            self.debug_object = {}
        else:
            self.debug_object = None

        return self._run_dsp(data, electronic_noise_data, electronic_shot_noise_data)

    @abc.abstractmethod
    def _run_special_dsp(
        self,
        electronic_noise_data: List[np.ndarray],
        electronic_shot_noise_data: List[np.ndarray],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Actually run the special DSP.

        Args:
            electronic_noise_data (List[np.ndarray]): electronic noise data.
            electronic_shot_noise_data (List[np.ndarray]): electronic and shot noise data.

        Returns:
            Tuple[np.ndarray, np.ndarray]: electronic noise symbols and electronic and shot noise symbols.
        """

    def special_dsp(
        self,
        electronic_noise_data: List[np.ndarray],
        electronic_shot_noise_data: List[np.ndarray],
    ) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """Applies the DSP on the electronic noise and electronic and shot noise.

        Args:
            electronic_noise_data (List[np.ndarray]): electronic noise data.
            electronic_shot_noise_data (List[np.ndarray]): electronic and shot noise data.

        Returns:
            Tuple[np.ndarray, np.ndarray]: electronic noise symbols and electronic and shot noise symbols.
        """

        if not self.special_parameters_set:
            logger.critical("Calling the DSP before the parameters are set.")
            return None

        return self._run_special_dsp(electronic_noise_data, electronic_shot_noise_data)

    def get_debug(self) -> Optional[Dict[str, Any]]:
        """Return the debug object.

        When calling this method with debug=False, results in returning the None object.

        Returns:
            Optional[Dict[str, Any]]: returns the debug object or None if debug=False.
        """
        if not self.debug:
            logger.warning(
                "Calling get_debug while debug=False in DSP results in getting a None object."
            )
        return self.debug_object
