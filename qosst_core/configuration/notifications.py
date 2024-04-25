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
Class for notifications Configuration.
"""
import logging
from typing import Dict, Type

from qosst_core.utils import get_object_by_import_path
from qosst_core.notifications import QOSSTNotifier
from qosst_core.configuration.base import BaseConfiguration
from qosst_core.configuration.exceptions import InvalidConfiguration

logger = logging.getLogger(__name__)


class NotificationsConfiguration(BaseConfiguration):
    """
    Class for notifications configuration. It should correspond to the notifications section.
    """

    notify: bool  #: Notifications are enabled with True and disabled with False.
    notifier: Type[QOSSTNotifier]  #: The notifier class.
    args: Dict  #: Dict of parameters to pass to the notifier class.

    DEFAULT_NOTIFY: bool = False  #: Default value for notify.
    DEFAULT_NOTIFIER_CLASS: str = (
        "qosst_core.notifications.FakeNotifier"  #: Default notifier class as str.
    )
    DEFAULT_ARGS: Dict = {}  #: Default parameters for the notifier class.

    def from_dict(self, config: Dict) -> None:
        """Fill the configuration from dict.

        Args:
            config (Dict): the dict corresponding to the notifications section.

        Raises:
            InvalidConfiguration: if the notifier class cannot be loaded.
            InvalidConfiguration: if the notifier class is not a subclass of :class:`qosst_core.notifications.QOSSTNotifier`.
        """
        self.notify = config.get("notify", self.DEFAULT_NOTIFY)
        notifier_class_str = config.get("notifier", self.DEFAULT_NOTIFIER_CLASS)

        try:
            self.notifier = get_object_by_import_path(notifier_class_str)
        except ImportError as exc:
            raise InvalidConfiguration(
                f"Cannot load authentication class {notifier_class_str}"
            ) from exc

        if not issubclass(self.notifier, QOSSTNotifier):
            raise InvalidConfiguration(
                f"Notifier class {notifier_class_str} is not a subclass of qosst_core.notifications.QOSSTNotifier."
            )
        self.args = config.get("args", self.DEFAULT_ARGS)

    def __str__(self) -> str:
        res = "=================================\n"
        res += "== Notifications Configuration ==\n"
        res += "=================================\n"
        res += f"Notify : {self.notify}\n"
        res += f"Notifier : {self.notifier}\n"
        res += f"Args : {self.args}\n"
        return res
