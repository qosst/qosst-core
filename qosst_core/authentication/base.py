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
Basic Authenticator classes.
"""
import abc


class BaseAuthenticator(abc.ABC):
    """The abstract class for Authenticators."""

    @abc.abstractmethod
    def sign_digest(self, digest: bytes) -> bytes:
        """Sign a digest.

        Args:
            digest (bytes): digest to sign.

        Returns:
            bytes: the signed digest.
        """

    @abc.abstractmethod
    def check_digest(self, digest: bytes, signed_digest: bytes) -> bool:
        """Check a signed digest.

        Args:
            digest (bytes): the unsigned digest.
            signed_digest (bytes): the signed digest.

        Returns:
            bool: True if the verification is successful, False, otherwise.
        """


class NoneAuthenticator(BaseAuthenticator):
    """
    Class for no Authentication.
    """

    def sign_digest(self, digest: bytes) -> bytes:
        """Sign a digest using the identity function

        Args:
            digest (bytes): the digest to sign.

        Returns:
            bytes: the signed digest.
        """
        return digest

    def check_digest(self, digest: bytes, signed_digest: bytes) -> bool:
        """Check the digest against itself (identity).

        Args:
            digest (bytes): the unsigned digest.
            signed_digest (bytes): the signed digest.

        Returns:
            bool: True if the two digits are equal, False otherwise.
        """
        return digest == signed_digest
