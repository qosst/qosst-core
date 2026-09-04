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
Maximum Length Sequence for synchronization
"""

import numpy as np

from qosst_core.synchronization.synchronization import SynchronizationSequence
from scipy.signal import max_len_seq


class MaximumLengthSequence(SynchronizationSequence):
    """
    Maximum Length Sequence class.
    """

    _nbits: int  #: number of bits of the sequence

    def __init__(self, nbits: int, **_kwargs) -> None:
        """
        Args:
            nbits (int): number of bits of the sequence
        """

        self._nbits = nbits

    def sequence(self) -> np.ndarray:
        """
        Generate the Maximum Length Sequence
        """

        return max_len_seq(nbits=self._nbits)[0]

    @property
    def length(self) -> int:
        """
        Length of the synchronization sequence
        """

        return (2**self._nbits) - 1

    def __repr__(self) -> str:
        return f"MaximumLengthSequence(nbits={self._nbits})"

    def __str__(self) -> str:
        return f"Maximum Length Sequence (nbits = {self._nbits})"
