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
This module contains the necessary codes to modulate and demodulate
data for the different modulations used in CV-QKD.

Here are some examples of use

.. code-block:: python

    from qosst_core.modulation import GaussianModulation, PSKModulation, QAMModulation, PCSQAMModulation

    # Create a Gaussian modulation with unit variance and 100 points
    gm = GaussianModulation(variance=1)
    points = gm.modulate(size=100)

    # Create a 16-PSK and with variance 2 and 1000 points
    pm = PSKModulation(variance=2, modulation_size=16)
    points = pm.modulate(size=1000)

    # Create a 256-QAM with variance 0.5 and 10000 points
    qm = QAMModulation(variance=0.5, modulation_size=256)
    points = qm.modulate(size=10000)

    # Create a PCS-1024-QAM with variance 5 and 100000 points
    pqm = PCSQAMModulation(variance=5, modulation_size=1024, nu=0.5)
    points = PCSQAMModulation(size=100000)
"""
from .modulation import Modulation

from .gaussian import GaussianModulation
from .psk import PSKModulation
from .qam import QAMModulation
from .pcsqam import PCSQAMModulation
from .singlepoint import SinglePointModulation
from .binomialqam import BinomialQAMModulation
