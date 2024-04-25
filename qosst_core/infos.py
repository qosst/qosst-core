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
File containing the logo (motd) and two utils function to print the motd and basic information.
"""
import sys
from typing import Optional

from qosst_core import __version__
from qosst_core.configuration import Configuration

# This metadata module is new from python3.8. For 3.7 we can try to import from the third-party module
# importlib-metadata
if sys.version_info.minor > 7:
    from importlib.metadata import version
    from importlib.metadata import PackageNotFoundError
else:
    try:
        from importlib_metadata import version
        from importlib_metadata import PackageNotFoundError
    except ModuleNotFoundError as exc:
        raise ImportError(
            "Python is version 3.7 and package importlib-metadata is not installed."
        ) from exc


MOTD: str = """

 ██████╗  ██████╗ ███████╗███████╗████████╗
██╔═══██╗██╔═══██╗██╔════╝██╔════╝╚══██╔══╝
██║   ██║██║   ██║███████╗███████╗   ██║   
██║▄▄ ██║██║   ██║╚════██║╚════██║   ██║   
╚██████╔╝╚██████╔╝███████║███████║   ██║   
 ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝  
                                                                                                                                         
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""


def get_script_infos(
    configuration: Optional[Configuration] = None, motd: bool = True
) -> str:
    """
    Get information on the current installed software for QOSST.

    Args:
        configuration (Configuration, optional): a configuration object that will be printed if given. Defaults to None.
        motd (bool, optional): if True, motd is included in the string, if False, it is not. Defaults to True.

    Returns:
        str: string containing MOTD, version information and optionnally cnfiguration information.
    """
    try:
        qosst_hal_version = version("qosst_hal")
    except PackageNotFoundError:
        qosst_hal_version = "Not installed"

    try:
        qosst_alice_version = version("qosst_alice")
    except PackageNotFoundError:
        qosst_alice_version = "Not installed"

    try:
        qosst_bob_version = version("qosst_bob")
    except PackageNotFoundError:
        qosst_bob_version = "Not installed"

    try:
        qosst_skr_version = version("qosst_skr")
    except PackageNotFoundError:
        qosst_skr_version = "Not installed"

    try:
        qosst_pp_version = version("qosst_pp")
    except PackageNotFoundError:
        qosst_pp_version = "Not installed"

    res: str = ""
    if motd:
        res += MOTD

    res += f"python version: {sys.version}\n\n"

    res += "QOSST versions\n"
    res += f"qosst_core: {__version__}\n"
    res += f"qosst_hal: {qosst_hal_version}\n"
    res += f"qosst_alice: {qosst_alice_version}\n"
    res += f"qosst_bob: {qosst_bob_version}\n"
    res += f"qosst_skr: {qosst_skr_version}\n"
    res += f"qosst_pp: {qosst_pp_version}\n"

    if configuration:
        res += "\n"
        res += str(configuration)
    return res
