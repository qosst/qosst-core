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
Definitions of detection schemas.
"""


class DetectionSchema:
    """
    Class representing a detection schema.

    The class holds the number of detectors that are required and wether or not it is implemented.
    """

    num_detectors: int  #: Number of detectors required for the detection schema.
    name: str  #: Readable name of the schema.
    implemented: bool  #: True if implemented, False otherwise.

    def __init__(
        self, num_detectors: int, name: str, implemented: bool = False
    ) -> None:
        """
        Args:
            num_detectors (int): number of required detectors.
            name (str): name of the detection schema
            implemented (bool, optional): True if implemented, False otherwise. Defaults to False.
        """
        self.num_detectors = num_detectors
        self.name = name
        self.implemented = implemented

    def check(self):
        """Check if the current detection schema can be used.

        Raises:
            NotImplementedError: if the detection is not implemented.
        """
        if not self.implemented:
            raise NotImplementedError(
                f"The detection scheme {self.name} is not implemented."
            )

    def __str__(self) -> str:
        return f"Detection schema : {self.name} (number of detectors : {self.num_detectors})"


SINGLE_POLARISATION_HOMODYNE = DetectionSchema(
    num_detectors=1, name="Homodyne - Single Polarisation", implemented=False
)  #: Detection scheme with one polarisation using homodyne detection (sifting).
SINGLE_POLARISATION_RF_HETERODYNE = DetectionSchema(
    num_detectors=1, name="RF Heterodyne - Single Polarisation", implemented=True
)  #: Detection scheme with one polarisation using RF heterodyne detection (one detector).
SINGLE_POLARISATION_PHASE_DIVERSE_HETERODYNE = DetectionSchema(
    num_detectors=2,
    name="Phase Diverse Heterodyne - Single Polarisation",
    implemented=False,
)  #: Detection scheme with one polarisation using phase diverse heterodyne detection (two detectors).

DOUBLE_POLARISATION_HOMODYNE = DetectionSchema(
    num_detectors=2, name="Homodyne - Double Polarisation", implemented=False
)  #: Detection scheme with two polarisations using homodyne detection (sifting).
DOUBLE_POLARISATION_RF_HETERODYNE = DetectionSchema(
    num_detectors=2, name="RF Heterodyne - Double Polarisation", implemented=False
)  #: Detection scheme with two polarisations using RF heterodyne detection (one detector per polarization).
DOUBLE_POLARISATION_PHASE_DIVERSE_HETERODYNE = DetectionSchema(
    num_detectors=4,
    name="Phase Diverse Heterodyne - Double Polarisation",
    implemented=False,
)  #: Detection scheme with two polarisations using phase diverse heterodyne detection (two detectors per polarization).
