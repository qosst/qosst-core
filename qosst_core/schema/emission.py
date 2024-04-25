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
Definition of emission schemas.
"""


class EmissionSchema:
    """
    Class representing an emission schema.

    The class holds the number of channels that are required and wether or not it is implemented.
    """

    num_channels: int  #: Number of channels required on the DAC.
    name: str  #: Readable name of the schema.
    implemented: bool  #: True if implemented, False otherwise.

    def __init__(self, num_channels: int, name: str, implemented: bool = False) -> None:
        """
        Args:
            num_channels (int): number of required channels.
            name (str): name of the emission schema.
            implemented (bool, optional): True if implemented, False otherwise. Defaults to False.
        """
        self.num_channels = num_channels
        self.name = name
        self.implemented = implemented

    def check(self) -> None:
        """Check if the emission schema can be used.

        Raises:
            NotImplementedError: if the emission schema is not implemented.
        """
        if not self.implemented:
            raise NotImplementedError(
                f"The emission schema {self.name} is not implemented."
            )

    def __str__(self) -> str:
        return (
            f"Emission schema : {self.name} (number of channels : {self.num_channels})"
        )


SINGLE_POLARISATION_SINGLE_SIDEBAND = EmissionSchema(
    num_channels=2, name="Single Polarisation - Single Sideband", implemented=True
)  #: Emission with encoding on one polarisation.
DOUBLE_POLARISATION_SINGLE_SIDEBAND = EmissionSchema(
    num_channels=4, name="Double Polarisation - Double Sideband", implemented=False
)  #: Emission with encoding on two polarisations.

SINGLE_POLARISATION_DOUBLE_SIDEBAND = EmissionSchema(
    num_channels=2, name="Single Polarisation - Double Sideband", implemented=False
)
DOUBLE_POLARISATION_DOUBLE_SIDEBAND = EmissionSchema(
    num_channels=4, name="Double Polarisation - Double Sideband", implemented=False
)

# For backward compatibility
SINGLE_POLARISATION = SINGLE_POLARISATION_SINGLE_SIDEBAND
DOUBLE_POLARISATION = DOUBLE_POLARISATION_SINGLE_SIDEBAND
