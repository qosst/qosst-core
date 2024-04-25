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
QOSST commands for the authentication submodule.
"""
import argparse

from qosst_core.authentication.falcon import FalconAuthenticator


def generate_falcon_key_pair(args: argparse.Namespace) -> bool:
    """Generate a Falcon key pair (public-private)

    Args:
        args (argparse.Namespace): args passed to the command line.

    Returns:
        bool: True if command was successful, False otherwise.
    """
    return FalconAuthenticator.generate_keys(
        size=args.size,
        directory=args.directory,
        secret_key_name=args.secret_key_name,
        public_key_name=args.public_key_name,
        force=args.force,
    )
