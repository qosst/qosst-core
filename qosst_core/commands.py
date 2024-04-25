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
This file will contain the code for script interactions.

It will call commands for the submodules.
"""
import argparse
import code
from typing import Optional

try:
    from IPython import start_ipython

    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False

from qosst_hal.utils import list_hardware_str
from qosst_core import __version__, RELEASE_NAME
from qosst_core.infos import MOTD, get_script_infos
from qosst_core.configuration.commands import (
    create_configuration_file_command,
)
from qosst_core.authentication.commands import generate_falcon_key_pair
from qosst_core.logging import create_loggers

THANKS_STRING = """
Thanks for using QOSST !

This is release {release_name} of QOSST.

We first thank the direct contributors of the code:
* Yoann Piétri
* Valentina Marulanda Acosta
* Matteo Schiavon
* Mayeul Chavanne
* Ilektra Karakosta - Amarantidou

We also thank all the persons that made comments and discussions that had a direct impact on this software:
* Luis-Trigo Vidarte
* Baptiste Gouraud
* Amine Rhouni
* Eleni Diamanti
* Philippe Grangier

And finally we thank the persons that participated in some ways to the development of QOSST:
* Thomas Liege
* George Crisan
* Damien Fruleux
* Sarah Layani
* Manon Huguenot
"""

# This part is a bit complicated, mainly to help generate the documentation automatically
# with the sphinx-argparse-cli package. This package does not support nested argparse.
# To go around this limitation, the nested subparsers are created in a function
# that takes as an optional parameter the parent parser. If a parent parser
# is present, we retrieve the subparsers element, add the parser and
# add subparsers to this parser. If the parent parser is not present
# we create a fake parser and add subparsers to this parser. So,
# if no parent is given (which will be the case when the documentation is
# generated), there is no nested subparsers.


def _create_main_parser() -> argparse.ArgumentParser:
    """
    Create the main parser.

    Commands:
        info (alias: versions)
        shell
        motd

    Returns:
        argparse.ArgumentParser: the main parser.
    """
    parser = argparse.ArgumentParser(prog="qosst")

    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Level of verbosity. If none, only critical errors will be prompted. -v will add warnings and errors, -vv will add info and -vvv will print all debug logs.",
    )

    subparsers = parser.add_subparsers()

    info_parser = subparsers.add_parser(
        "info", aliases=["versions"], help="Display info on the package"
    )
    info_parser.set_defaults(func=info)

    shell_parser = subparsers.add_parser("shell", help="Start a shell")
    shell_parser.set_defaults(func=shell)

    motd_parser = subparsers.add_parser("motd", help="Print MOTD")
    motd_parser.set_defaults(func=motd)

    credits_parser = subparsers.add_parser("credits", help="Credits of QOSST")
    credits_parser.set_defaults(func=qosst_credits)

    hardware_parser = subparsers.add_parser(
        "hardware", help="List the hardware of a given package"
    )
    hardware_parser.set_defaults(func=print_hardware)
    hardware_parser.add_argument("package", help="Name of the package to inspect")
    return parser


def _create_configuration_parser(
    parent_parser: Optional[argparse.ArgumentParser] = None,
) -> argparse.ArgumentParser:
    """Create the configuration parser.

    If parent_parser is present, the configuration parser is added in
    the subparsers of the parent parser. If not, another parser
    is created. parent_parser not present should only be used for
    documentation.

    Commands:
        create
        check

    Args:
        parent_parser (argparse.ArgumentParser, optional): parent parser to use. Defaults to None.

    Returns:
        argparse.ArgumentParser: configuration parser.
    """
    if parent_parser:
        # pylint: disable=protected-access
        assert (
            parent_parser._subparsers
        )  # At this point, we should find the subparsers.
        subparsers = parent_parser._subparsers._group_actions[0]
        assert isinstance(
            subparsers, argparse._SubParsersAction
        )  # We could have got a general action, check that it's inded a subparsers action.
        configuration_parser = subparsers.add_parser(
            "configuration", help="Configuration commands"
        )
        configuration_subparsers = configuration_parser.add_subparsers()
    else:
        parser = argparse.ArgumentParser(prog="qosst configuration")
        configuration_subparsers = parser.add_subparsers()

    configuration_create_parser = configuration_subparsers.add_parser(
        "create", help="Create a configuration file"
    )
    configuration_create_parser.set_defaults(func=create_configuration_file_command)
    configuration_create_parser.add_argument(
        "-f",
        "--file",
        default="config.toml",
        help="Path of the file to create. Default : config.toml.",
    )
    configuration_create_parser.add_argument(
        "--override",
        action="store_true",
        help="If present, this will override the current configuration file at the given path, if it exists.",
    )

    if parent_parser:
        return parent_parser
    return parser


def _create_auth_parser(parent_parser: Optional[argparse.ArgumentParser] = None):
    """Create the auth parser.

    If parent_parser is present, the auth parser is added in
    the subparsers of the parent parser. If not, another parser
    is created. parent_parser not present should only be used for
    documentation.

    Commands:
        generate-falcon

    Args:
        parent_parser (argparse.ArgumentParser, optional): parent parser to use. Defaults to None.

    Returns:
        argparse.ArgumentParser: auth parser.
    """
    if parent_parser:
        # pylint: disable=protected-access
        assert (
            parent_parser._subparsers
        )  # At this point, we should find the subparsers.
        subparsers = parent_parser._subparsers._group_actions[0]
        assert isinstance(
            subparsers, argparse._SubParsersAction
        )  # We could have got a general action, check that it's inded a subparsers action.
        authentication_parser = subparsers.add_parser(
            "auth", help="Authentication commands"
        )
        authentication_parser_subparsers = authentication_parser.add_subparsers()
    else:
        parser = argparse.ArgumentParser(prog="qosst auth")
        authentication_parser_subparsers = parser.add_subparsers()

    authentication_create_falcon_keypair = authentication_parser_subparsers.add_parser(
        "generate-falcon", help="Generate a Falcon keypair."
    )
    authentication_create_falcon_keypair.add_argument(
        "-n", "--size", default=512, type=int, help="Size of the falcon key."
    )
    authentication_create_falcon_keypair.add_argument(
        "-d", "--directory", default="keys", help="Directory where to save keys."
    )
    authentication_create_falcon_keypair.add_argument(
        "-s",
        "--secret-key-name",
        default="secret_key.json",
        help="Name of the secret key file.",
    )
    authentication_create_falcon_keypair.add_argument(
        "-p",
        "--public-key-name",
        default="public_key.json",
        help="Name of the public key file.",
    )
    authentication_create_falcon_keypair.add_argument(
        "-f", "--force", action="store_true", help="Overwrite existing files."
    )
    authentication_create_falcon_keypair.set_defaults(func=generate_falcon_key_pair)
    if parent_parser:
        return parent_parser
    return parser


# pylint: disable=too-many-locals
def main():
    """
    This is the actual entrypoint.

    It will construct the parser and subparsers for the different command.
    """
    parser = _create_main_parser()
    _create_configuration_parser(parser)
    _create_auth_parser(parser)

    args = parser.parse_args()
    create_loggers(args.verbose, None)

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("No command specified. Run with -h|--help to see the possible commands.")


def info(_args: argparse.Namespace) -> bool:
    """Print information on the current installation of cvqkd_core

    Args:
        _args (argparse.Namespace): the args passed to the command line.

    The args are not used.

    Returns:
        bool: this function always returns True.
    """
    print(get_script_infos())
    return True


def shell(_args: argparse.Namespace) -> bool:
    """Start a shell.

    The shell will be using IPython if available and
    fallback on the default interactive shell if not.

    Args:
        _args (argparse.Namespace): the args passed to the command line.

    The args are not used.

    Returns:
        bool: this function always returns True.
    """
    print(MOTD)
    if IPYTHON_AVAILABLE:
        start_ipython(argv=[])
    else:
        console = code.InteractiveConsole()
        console.interact(exitmsg="See you soon for CV-QKD.")
    return True


def motd(_args: argparse.Namespace) -> bool:
    """Print only the motd (logo)

    Args:
        _args (argparse.Namespace): the args passed to the command line.

    The args are not used.

    Returns:
        bool: this function always returns True.
    """
    print(MOTD)
    return True


def qosst_credits(_args: argparse.Namespace) -> bool:
    """Print the thank message.

    Args:
        _args (argparse.Namespace): the args passed to the command line.

    The args are not used.

    Returns:
        bool: this function always returns True.
    """
    print(MOTD)
    print(THANKS_STRING.format(release_name=RELEASE_NAME))
    return True


def print_hardware(args: argparse.Namespace) -> bool:
    """Print the hardware of a given HAL module using the utils
    function list_hardware_str from qosst_hal.

    Args:
        args (argparse.Namespace): the args passed to the command line.

    Returns:
        bool: this function always returns True.
    """
    print(list_hardware_str(args.package))
    return True


if __name__ == "__main__":
    main()
