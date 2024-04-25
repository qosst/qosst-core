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
Class for authentication using the Falcon algorithm (PQC)
"""
import logging
import os
import json
from pathlib import Path
from typing import List

from falcon import falcon

from qosst_core.authentication.base import BaseAuthenticator

logger = logging.getLogger(__name__)


class FalconAuthenticator(BaseAuthenticator):
    """Class for the Falcon Authenticator."""

    secret_key: "falcon.SecretKey"

    def __init__(
        self,
        secret_key: List[List[int]],
        remote_public_key: List[int],
    ) -> None:
        """
        Args:
            secret_key (List[List[int]]): secret key (to sign digests).
            remote_public_key (List[int]): public key of the remote party (to check digests).
        """
        logger.debug("Initializing FalconAuthenticator")
        size: int = len(secret_key[0])
        self.secret_key = falcon.SecretKey(size, secret_key)
        self.remote_public_key = falcon.PublicKey(size, remote_public_key)

    def sign_digest(self, digest: bytes) -> bytes:
        """Sign a digest using the secret_key.

        Args:
            digest (bytes): digest to sign.

        Returns:
            bytes: the signed digest.
        """
        logger.debug("Signing digest")
        return self.secret_key.sign(digest)

    def check_digest(self, digest: bytes, signed_digest: bytes) -> bool:
        """Check a signed digest again the remote_public_key.

        Args:
            digest (bytes): the unsigned digest.
            signed_digest (bytes): the signed digest.

        Returns:
            bool: True if the verification is successful, False otherwise.
        """
        logger.debug("Checking digest")
        return self.remote_public_key.verify(digest, signed_digest)

    @staticmethod
    def generate_keys(
        size: int = 512,
        directory: str = "keys",
        secret_key_name: str = "secret_key.json",
        public_key_name: str = "public_key.json",
        force=False,
    ) -> bool:
        """Generate a new key-pair.

        Args:
            size (int, optional): size of the key. Defaults to 512.
            directory (str, optional): directory where to save the key. Defaults to "keys".
            secret_key_name (str, optional): name of the secret key file. Defaults to "secret_key.json".
            public_key_name (str, optional): name of the public key file. Defaults to "public_key.json".
            force (bool, optional): if True, the script will overwrite pre-existing keys. Defaults to False.

        Returns:
            bool: True if the generation was successful, False otherwise.
        """
        logger.info("Generating a new private-public key pair.")
        logger.info("Checking if files exist.")

        path_sk = Path(directory) / secret_key_name
        path_pk = Path(directory) / public_key_name

        if os.path.isfile(path_sk):
            logger.warning("File exists at %s.", str(path_sk))

        if os.path.isfile(path_pk):
            logger.warning("File exists at %s.", str(path_pk))

        if (os.path.isfile(path_sk) or os.path.isfile(path_pk)) and not force:
            logger.error(
                "At least one file exists and force is False. Aborting generation."
            )
            return False

        logger.info("Checking if dir exists")
        if not os.path.isdir(directory):
            logger.warning(
                "Directory %s does not exist. Attempting to create it.", directory
            )
            try:
                os.mkdir(directory)
            except IOError as exc:
                logger.error("Cannot create directory: %s", str(exc))
                return False

        logger.info("Generating secret key with n = %i", size)
        secret_key = falcon.SecretKey(n=size)
        logger.info("Secret key generated.")

        logger.info("Saving secret key at %s.", str(path_sk))
        with open(path_sk, "w", encoding="utf-8") as file_descriptor:
            json.dump(
                [secret_key.f, secret_key.g, secret_key.F, secret_key.G],
                file_descriptor,
            )

        logger.info("Secret key saved.")

        logger.info("Saving publing key at %s.", str(path_pk))
        with open(path_pk, "w", encoding="utf-8") as file_descriptor:
            json.dump(secret_key.h, file_descriptor)

        logger.info("Key pair generated.")
        return True
