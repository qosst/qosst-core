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
File containing the default push key method.
"""

import uuid
from typing import List

import logging

logger = logging.getLogger(__name__)


def default_push_key(
    key_material_id: uuid.UUID, key_material: List[int], **_kwargs
) -> bool:
    """Dummy push key function.

    Args:
        key_material_id (uuid.UUID): uuid of the key material.
        key_material (List[int]): key material.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    logger.info(
        "Pushing key %s (len %i) to nowhere... Consider using an acutal push key interface",
        str(key_material_id),
        len(key_material),
    )
    return True
