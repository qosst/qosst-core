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
This file contains function that will be called from the main command of qosst_core.
"""
import argparse
import shutil
from pathlib import Path


def create_configuration_file_command(args: argparse.Namespace) -> bool:
    """
    Command to create a configuration file from the config.example.toml file.

    Args:
        args (argparse.Namespace): args passed from the command line.

    The args should contain :

        * file(str): the path of the file to create.
        * override(bool): if True, this will override the file at the path if it exists.


    Returns:
        bool: True if the operation was successful, False otherwise
    """
    return create_configuration_file(file=args.file, override=args.override)


def create_configuration_file(file: str, override: bool = False) -> bool:
    """Create a configuration file from the config.example.toml file.

    Args:
        file (str): the path of the file to create
        override (bool, optional): if True, it will the override at the given path, if it exists. Defaults to False.

    Returns:
        bool: True if the creation was successful, False otherwise.
    """
    path = Path(file)

    # Check if the file exists
    if path.is_file():
        if override:
            print("[WARNING] The file {path} already exists. Overriding it...\n")
        else:
            print(
                "[ERROR] Wooops ! The file {path} already exists. If you want to override it, use the '--override' parameter.\n"
            )
            return False

    # Now let's create the file
    try:
        template_path = Path(__file__).parent / "config.example.toml"
        shutil.copyfile(template_path, path)
    except (shutil.SameFileError, IOError) as excp:
        print(
            f"[ERROR] There was an error copying the file. Here is the exception : {excp}.\n"
        )
        return False
    print(f"[OK] Default config was copied to {path}.\n")
    return True
