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
Configuration for the post_processing section.
"""

from typing import Type
import logging

from qosst_core.configuration.exceptions import (
    InvalidConfiguration,
)
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.utils import get_object_by_import_path
from qosst_core.extractors import RandomnessExtractor

logger = logging.getLogger(__name__)


class ReconciliationConfiguration(BaseConfiguration):
    """
    Configuration for the error reconciliation step.
    It should correspond to the post_processing.reconciliation section.
    """

    beta: float  #: Efficiency of the error reconciliation code.
    dimension: float  #: Dimension of the multi-dimensional reconciliation.
    remote: bool  #: Use the reconciliation procedure with a remote worker.
    remote_endpoint: str  #: Endpoint to use for the remote worker.

    DEFAULT_BETA: float = 0.95  #: Default value of the error reconciliation code.
    DEFAULT_DIMENSION: int = 8  #: Default dimension of the error reconciliation code.
    DEFAULT_REMOTE: bool = False  #: Default remote reconciliation.
    DEFAULT_REMOTE_ENDPOINT: str = (
        ""  #: Default endpoint for the remote reconciliation.
    )

    def from_dict(self, config):
        self.beta = config.get("beta", self.DEFAULT_BETA)
        self.dimension = config.get("dimension", self.DEFAULT_DIMENSION)
        self.remote = config.get("remote", self.DEFAULT_REMOTE)
        self.remote_endpoint = config.get(
            "remote_endpoint", self.DEFAULT_REMOTE_ENDPOINT
        )

        if not isinstance(self.beta, float) or self.beta < 0 or self.beta > 1:
            raise InvalidConfiguration(
                f"{self.beta} is a valid value for beta (it should be a float between 0 and 1)."
            )

        if not isinstance(self.dimension, int) or self.dimension not in [1, 2, 4, 8]:
            raise InvalidConfiguration(
                f"{self.dimension} is not a valid value for the dimension of the multi-dimensional scheme. It should be 1,2,4 or 8."
            )

    def __str__(self) -> str:
        res = "Error Reconciliation Configuration\n"
        res += "----------------------------------\n"
        res += f"beta : {self.beta}\n"
        res += f"Dimension : {self.dimension}\n"
        res += f"Remote : {self.remote}\n"
        res += f"Remote endpoint : {self.remote_endpoint}\n"
        res += "\n"
        return res


class PrivacyAmplificationConfiguration(BaseConfiguration):
    """
    Configuration for the privacy amplification step.
    It should correspond to the post_processing.privacy_amplification section.
    """

    extractor: Type[
        RandomnessExtractor
    ]  #: The extractor class for privacy amplification.

    DEFAULT_EXTRACTOR_STR: str = (
        "qosst_core.extractors.DummyExtractor"  #: Default dummy randomness extractor.
    )

    def from_dict(self, config: dict) -> None:
        """Fill instance from dict.

        Args:
            config (dict): dict correspoding to the post_processing.privacy_amplification section.

        Raises:
            InvalidConfiguration: if the extractor class canoot be loaded.
            InvalidConfiguration: if the extractor class is not a subclass of :class:`qosst_core.extractors.RandomnessExtractor`.
        """
        extractor_str = config.get("extractor", self.DEFAULT_EXTRACTOR_STR)
        try:
            self.extractor = get_object_by_import_path(extractor_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Impossible to load the extractror {extractor_str}."
            ) from exc

        if not issubclass(self.extractor, RandomnessExtractor):
            raise InvalidConfiguration(
                f"{extractor_str} is not a subclass of RandomnessExtractor."
            )

    def __str__(self) -> str:
        res = "Privacy Amplification Configuration\n"
        res += "-----------------------------------\n"
        res += f"Extractor : {self.extractor}\n"
        res += "\n"
        return res


class PostProcessingConfiguration(BaseConfiguration):
    """
    The post processing configuration. It should correspond to the post_processing section.
    """

    reconciliation: ReconciliationConfiguration  #: The post processing error reconciliation configuration.
    privacy_amplification: PrivacyAmplificationConfiguration  #: The post processing privacy amplfication configuration.

    def from_dict(self, config: dict) -> None:
        """Fill instance from the config.

        Args:
            config (dict): dict corresponding to the post_processing section.
        """
        if "reconciliation" not in config:
            logger.warning(
                "post_processing.reconciliation is missing from the configuration file. Using default values for all the parameters."
            )
        if "privacy_amplification" not in config:
            logger.warning(
                "post_processing.privacy_amplification is missing from the configuration file. Using default values for all the parameters."
            )

        self.reconciliation = ReconciliationConfiguration(
            config.get("reconciliation", {})
        )

        self.privacy_amplification = PrivacyAmplificationConfiguration(
            config.get("privacy_amplification", {})
        )

    def __str__(self) -> str:
        res = "===================================\n"
        res += "== Post Processing Configuration ==\n"
        res += "===================================\n"
        res += str(self.reconciliation)
        res += str(self.privacy_amplification)
        return res
