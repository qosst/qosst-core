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
qosst-core module for logging. In particular, it contains
a function to go from the verbosity level to the log level and 
a function to create loggers.
"""
import logging
from typing import Tuple, Optional

from qosst_core.configuration import Configuration
from qosst_core.utils import QOSSTPath


def verbose_to_log_level(verbose: int) -> int:
    """Return the log level (as int), depending on
    the verbosity level (corresponding to the numbers of -v
    given in parameter).

    0 -v : Only display critical logs.
    1 -v : Display critical, error and warning logs.
    2 -v : Display critical, error, warning and info logs.
    3 or more -v : Display every log.

    Args:
        verbose (int): the verbosity level.

    Returns:
        int: the log level.
    """
    if verbose == 0:
        return logging.CRITICAL

    if verbose == 1:
        return logging.WARNING

    if verbose == 2:
        return logging.INFO

    return logging.DEBUG


def create_loggers(
    verbose: int, configuration_path: QOSSTPath
) -> Tuple[logging.Logger, logging.Handler, Optional[logging.Handler]]:
    """Get the root logger and add a console handler (using
    the verbosity level) and a file handler (using the
    configuration).

    Args:
        verbose (int): the verbosity level.
        configuration_path (QOSSTPath): the path of the configuration path. If None, same behaviour as if file logging was disabled.

    Returns:
        Tuple[logging.Logger, logging.Handler, logging.Handler]: the root logger, the console handler and the file hander (None if file logging was disabled).
    """
    console_log_level = verbose_to_log_level(verbose)

    if configuration_path:
        configuration = Configuration(configuration_path)

    if configuration_path and configuration.logs.logging:
        root_log_level = min(console_log_level, configuration.logs.level)
    else:
        root_log_level = console_log_level

    root_logger = logging.getLogger("")
    root_logger.setLevel(root_log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if configuration_path and configuration.logs.logging:
        file_handler = logging.FileHandler(configuration.logs.path)
        file_handler.setLevel(configuration.logs.level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    else:
        file_handler = None

    return root_logger, console_handler, file_handler
