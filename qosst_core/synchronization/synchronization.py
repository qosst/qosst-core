# qosst-core - Core module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2025 Matteo Schiavon

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
Generic synchronization sequence.
"""
import abc
from typing import Optional

import numpy as np


# pylint: disable=too-few-public-methods
class SynchronizationSequence(abc.ABC):
    """
    Abstract class for the synchronization sequence.
    """

    def __init__(self, **_kwargs) -> None:
        pass

    @abc.abstractmethod
    def sequence(self) -> np.ndarray:
        """
        Generate the synchronization sequence.

        Returns:
            np.ndarray: the modulated points.
        """

    @property
    @abc.abstractmethod
    def length(self) -> int:
        """
        Return the length of the synchronization sequence.
        
        Returns:
            int: length of the synchronization sequence.
        """