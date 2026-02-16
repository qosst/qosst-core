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
This module contains the necessary codes for generating the syncrhonization
sequence.

Here are some examples of use

.. code-block:: python

    from qosst_core.synchronization import ZadoffChuSequence, MaximumLengthSequence

    # Create a Zadoff-Chu synchronization sequence with root 5 and length 3989
    zc = ZadoffChuSequence(root=5, length=3989)
    sequence = zc.sequence()

    # Create a Maximum Length Sequence with 16 bits
    mls = MaximumLengthSequence(nbits=16)
    sequence = mls.sequence()

"""
from .synchronization import SynchronizationSequence

from .zc import ZadoffChuSequence
from .mls import MaximumLengthSequence