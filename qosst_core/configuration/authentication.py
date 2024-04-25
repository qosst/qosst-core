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
Class for Authentication Configuration.
"""
import logging
import re
import json
from typing import Dict, Type

from qosst_core.utils import get_object_by_import_path
from qosst_core.authentication.base import BaseAuthenticator
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.configuration.exceptions import InvalidConfiguration

logger = logging.getLogger(__name__)


class AuthenticationConfiguration(BaseConfiguration):
    """
    Class for Authentication Configuration. It should be initialized with the authentication section.
    """

    authentication_class: Type[BaseAuthenticator]  #: The authentication class.
    authentication_params: (
        Dict  #: Dict of parameters to pass to the authentication class.
    )

    DEFAULT_AUTHENTICATION_CLASS: str = (
        "qosst_core.authentication.NoneAuthenticator"  #: Default authentication class as str.
    )
    DEFAULT_AUTHENTICATION_PARAMS: Dict = (
        {}
    )  #: Default parameters for the authentication class.

    def from_dict(self, config: Dict) -> None:
        """Load the class from a dict. The dict should correspond to the authentication section.

        For the authentication_params, if the from_file key is present, the value is loaded from the file
        as a json object. The value associated with the from_file key (which was before the path of the file)
        is replaced with the loaded value from the file.

        Args:
            config (Dict): the authentication section of the configuration file.

        Raises:
            InvalidConfiguration: if the authentication class cannot be loaded.
            InvalidConfiguration: if the authentication class is not a subclass of :class:`qosst_core.authenticator.BaseAuthenticator`.
            InvalidConfiguration: if the from_file argument was present in the authentication_params and that the file was not readable.
        """
        authentication_class_str = config.get(
            "authentication_class", self.DEFAULT_AUTHENTICATION_CLASS
        )

        try:
            self.authentication_class = get_object_by_import_path(
                authentication_class_str
            )
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load authentication class {authentication_class_str}"
            ) from exc

        if not issubclass(self.authentication_class, BaseAuthenticator):
            raise InvalidConfiguration(
                f"Authentication class {authentication_class_str} is not a subclass of qosst_core.authenticator.BaseAuthenticator."
            )
        self.authentication_params = config.get(
            "authentication_params", self.DEFAULT_AUTHENTICATION_PARAMS
        )

        # Transforms the from_file
        for key, value in self.authentication_params.items():
            result = re.search(r"^from_file\((.*)\)$", value)
            if result:
                filename = result.group(1)
                logger.info("Reading value from file: %s", filename)

                try:
                    with open(filename, "r", encoding="utf-8") as file_descriptor:
                        self.authentication_params[key] = json.load(file_descriptor)
                except (IOError, json.JSONDecodeError) as exc:
                    raise InvalidConfiguration(
                        f"Error when reading the file {filename}"
                    ) from exc

    def __str__(self) -> str:
        res = "==================================\n"
        res += "== Authentication Configuration ==\n"
        res += "==================================\n"
        res += f"Authentication class : {self.authentication_class}\n"
        res += f"Authentication params (contains) : {', '.join(self.authentication_params.keys())}\n"
        return res
