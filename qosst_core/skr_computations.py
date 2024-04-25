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
Definition of BaseCVQKDSKRCalculator for qosst_skr.

Definition of NoneSKRCalculator for the configuration.
"""
import abc


# pylint: disable=too-few-public-methods
class BaseCVQKDSKRCalculator(abc.ABC):
    """
    This is a base calculator, that is not calculating anything.
    Every calculator should inherit from this base calculator.

    No proof is provided for this calculator.
    No link is available for this calculator.
    """

    @staticmethod
    @abc.abstractmethod
    def skr(**kwargs) -> float:
        """
        Static method to compute the Secret Key Rate depending on the calculator.

        Returns:
            float: the secret key rate in bits per symbol.
        """


class NoneSKRCalculator(BaseCVQKDSKRCalculator):
    """
    NoneSKRCalculator.

    Always return 0 for the SKR.
    """

    @staticmethod
    def skr(**kwargs) -> float:
        """
        SKR calculator for the none calculator.

        All parameters are ignored.

        Returns:
            float: 0
        """
        return 0.0
