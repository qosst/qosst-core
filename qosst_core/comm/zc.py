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
Zadoff-Chu sequence for synchronisation.
"""

import numpy as np


def zcsequence(root: int, length: int, cyclic_shift: int = 0) -> np.ndarray:
    """This function implements a Zadoff-Chu sequence.

    It takes as input the parameters of the sequence and returns the sequence in a np array.

    Args:
        root (int): the root of the Zadoff-Chu sequence. Often named u.
        length (int): the length of the Zadoff-Chu sequence. Often named Nzc.
        cyclic_shift (int, optional): the cyclic shift of the Zadoff-Chu sequence. Often named q. Defaults to 0.

    Raises:
        ValueError: when the root is not strictly between 0 and length.
        ValueError: when the root and the length are not coprimes.

    Returns:
        np.ndarray: the generated Zadoff-Chu sequence.
    """
    # Verifications for the Zadoff-Chu sequence.
    if root <= 0 or root >= length:
        raise ValueError(
            f"The root should be 0 < root < length (root={root}, length = {length})."
        )
    if np.gcd(root, length) != 1:
        raise ValueError(
            f"The root and length are not coprime (gcd(root={root}, length={length}) = {np.gcd(root, length)})."
        )

    # Now generate the sequence
    time = np.arange(length)

    return np.exp(
        -1j * (np.pi * root * time * (time + length % 2 + 2 * cyclic_shift)) / length
    )
