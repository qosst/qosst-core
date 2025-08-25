# qosst-core - Core module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2025 Yoann Piétri

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
Module defining the base class RandomnessExtractor for privacy amplification.

Implementations of actual extractors are in qosst-pp.
"""

import abc
import random
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


class RandomnessExtractor(abc.ABC):
    """
    A generic randomness extractor.
    """

    reconciled_key_size: int
    final_key_size: int

    def __init__(self, reconciled_key_size: int, final_key_size: int) -> None:
        """Initialization method.

        Args:
            reconciled_key_size (int): length of the input reconciled key.
            final_key_size (int): length of the output final key.
        """
        if final_key_size > reconciled_key_size:
            logger.error("Final key size is strictly greater than reconciled key size.")
        self.reconciled_key_size = reconciled_key_size
        self.final_key_size = final_key_size
        super().__init__()

    @property
    @abc.abstractmethod
    def seed_size(self) -> int:
        """Return the necessary seed side, depeding on the extractor.
        The seed size is computed using the reconciled key size and
        the final key size

        Returns:
            int: the seed size.
        """

    @staticmethod
    def generate_seed(seed_length: int) -> List[int]:
        """Generate a seed, i.e. a list of random binaries.

        Args:
            seed_length (int): length of the seed to generate.

        Returns:
            List[int]: seed.
        """
        logger.debug("Generatind seed of length %i", seed_length)
        return [random.randint(0, 1) for _ in range(seed_length)]

    def extract(self, reconciled_key: List[int], seed: Optional[List[int]] = None):
        """Extract randomness from the input reconciled key, using the seed.

        If seed is None, a new seed is genrerated using
        the static function {py:func}`qosst_core.extractors.RandomnessExtractor.generate_seed`
        and is returned with the extracted data.

        Args:
            reconciled_key (List[int]): the reconciled key data.
            seed (Optional[List[int]], optional): seed for the extractor. Defaults to None.

        Returns:
            Tuple[Optional[List[int]], Optional[List[int]]]: final extracted key and seed.
        """

        if seed is None:
            seed = self.generate_seed(self.seed_size)
        else:
            if len(seed) != self.seed_size:
                logger.error(
                    "Seed length is incorrect (%i != %i). Aborting extraction.",
                    self.seed_size,
                    len(seed),
                )
                return None, None

        return self._extract(reconciled_key, seed)


    @abc.abstractmethod
    def _extract(
        self, reconciled_key: List[int], seed: List[int]
    ) -> Tuple[Optional[List[int]], Optional[List[int]]]:
        """Actually perform extraction from the input reconciled key, using the seed.

        Args:
            reconciled_key (List[int]): the reconciled key data.
            seed (Optional[List[int]]): seed for the extractor.

        Returns:
            Tuple[Optional[List[int]], Optional[List[int]]]: final extracted key and seed.
        """


class DummyExtractor(RandomnessExtractor):
    """
    A dummy extractor to serve as a default value.

    Only returns the intial key, until length final_key_size.
    """

    @property
    def seed_size(self) -> int:
        return 0

    def _extract(self, reconciled_key: List[int], seed: List[int]):
        logger.warning(
            "This is not a true extractor and is solely returning the same key as the input."
        )

        return reconciled_key[: self.final_key_size]
