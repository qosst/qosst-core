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
Exceptions for the reading of the configuration file.
"""


class InvalidConfiguration(Exception):
    """
    Base exception for an invalid configuration of CVQKD.
    """

    message: str

    def __init__(self, message: str = "") -> None:
        """
        Args:
            message (str, optional): error message. Defaults to "".
        """
        self.message = message

    def __str__(self) -> str:
        """Error message.

        Returns:
            str: error message.
        """
        return f"Invalid configuration: {self.message}"


class InvalidTime(InvalidConfiguration):
    """
    Exception raised when a time in the configuration is invalid.
    """

    time: float  #: the time that is not right.

    def __init__(self, time: float) -> None:
        """Initialization function.

        Args:
            time (float): the time that is not right.
        """
        self.time = time
        super().__init__()

    def __str__(self) -> str:
        """Error message

        Returns:
            str: error message.
        """
        return (
            f"Time must either be a strictly positive number or 0 (input : {self.time})"
        )


class InvalidClockMaster(InvalidConfiguration):
    """
    Exception for invalid clock master.
    """

    given_master: str

    def __init__(self, given_master: str) -> None:
        """Initialization function.

        Args:
            given_master (str): master given in the configuration file.
        """
        self.given_master = given_master
        super().__init__()

    def __str__(self) -> str:
        return f"{self.given_master} is not a valid master for clock sharing. Valid masters are alice and bob."


class InvalidEta(InvalidConfiguration):
    """Exception for invalid eta in the configuration file.

    Args:
        eta (float): eta given in the configuration file.
    """

    def __init__(self, eta: float) -> None:
        """Initialization function.

        Args:
            eta (float): eta given in the configuration file.
        """
        self.eta = eta
        super().__init__()

    def __str__(self) -> str:
        return f"The value of η (eta) : {self.eta} is not between 0 and 1."
