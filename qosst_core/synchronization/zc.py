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
Zadoff-Chu synchronization sequence
"""
import numpy as np

from qosst_core.synchronization.synchronization import SynchronizationSequence
from qosst_core.comm.zc import zcsequence

class ZadoffChuSequence(SynchronizationSequence):
    """
    Zadoff-Chu synchronization sequence.
    """

    _root: int  #: Root value for the sequence.
    _length: int  #: Length of the sequence.

    def __init__(self, root: int, length: int, **_kwargs) -> None:
        """
        Args:
            root (int): the root of the Zadoff-Chu sequence.
            length (int): the length of the Zadoff-Chu sequence.
        """

        self._root = root
        self._length = length
            
    def sequence(self) -> np.ndarray:
        """
        Generate the Zadoff-Chu sequence
        """

        return zcsequence(root=self._root, length=self._length)
    
    @property
    def length(self) -> int:
        """
        Length of the synchronization sequence
        """

        return self._length
    
    def __repr__(self) -> str:
        return f"ZadoffChuSequence(root={self._root},length={self._length})"

    def __str__(self) -> str:
        return f"Zadoff Chu sequence (root = {self._root}, length = {self._length})"