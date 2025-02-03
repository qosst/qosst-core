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


class PrivacyAmplficationConfiguration(BaseConfiguration):
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

    privacy_amplification: PrivacyAmplficationConfiguration  #: The post processing privcay amplfication configuration.

    def from_dict(self, config: dict) -> None:
        """Fill instance from the config.

        Args:
            config (dict): dict corresponding to the post_processing section.
        """
        if "privacy_amplification" not in config:
            logger.warning(
                "post_processing.privacy amplification is missing from the configuration file. Using default values for all the parameters."
            )

        self.voa = PrivacyAmplficationConfiguration(
            config.get("privacy_amplification", {})
        )

    def __str__(self) -> str:
        res = "===================================\n"
        res += "== Post Processing Configuration ==\n"
        res += "===================================\n"
        res += str(self.voa)
        return res
