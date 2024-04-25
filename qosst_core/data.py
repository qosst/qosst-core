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
Module to handle object that should be saved and loaded in QOSST.
"""
from typing import Optional
import pickle
import logging
import datetime

from qosst_core.utils import QOSSTPath

logger = logging.getLogger(__name__)


class BaseQOSSTData:
    """
    A basic class to create loadable and dumpable
    (non human-readable) object using pickle.

    The class as a dump (alias save) method so
    an instance can be save as simple as calling this method.
    There is also a static method to load an object from a file
    that return an instance of this object.

    Example:

    .. code-block:: python

        from qosst_core.data import BaseQOSSTData

        class MyData(BaseQOSSTData):
            x: int
            def __init__(self, x:int):
                self.x = x

        my_object = MyData(x=3)
        type(my_object) # MyData
        my_object.x # 3

        my_object.save("test")

        my_object2 = MyData.load("test")
        type(my_object2) # MyData
        my_object2.x # 3

    """

    _saved_path: Optional[
        QOSSTPath
    ]  #: Path were the object was saved to or loaded from.
    _saved_datetime: Optional[datetime.datetime]  #: Datetime of the last save.
    _loaded: bool  #: True if the object was loaded from a file, False otherwise.

    @staticmethod
    def load(path: QOSSTPath):
        """
        Load from file and return an instance of the class.

        Args:
            path (QOSSTPath): the path of the file to load.

        Returns:
            Self: an instance of the current class.
        """
        try:
            with open(path, "rb") as file:
                obj = pickle.load(file)
                logging.info(
                    "Loaded object from location %s",
                    str(path),
                )
                obj.set_loaded()
                return obj
        except IOError as exc:
            logger.critical(
                "Loading object at location %s failed: %s", str(path), str(exc)
            )
            return None

    def dump(self, path: QOSSTPath) -> None:
        """
        Dump the current object to a file.

        Args:
            path (QOSSTPath): the path where to save the data.
        """

        try:
            with open(path, "wb") as file:
                self._saved_datetime = datetime.datetime.now()
                self._saved_path = path
                self._loaded = False
                pickle.dump(self, file)
                logging.info(
                    "Saved instance of class %s to location %s",
                    self.__class__.__name__,
                    str(path),
                )
        except IOError as exc:
            self._saved_datetime = None
            self._saved_path = None
            logger.critical(
                "Saving object to location %s failed: %s", str(path), str(exc)
            )

    def save(self, path: QOSSTPath) -> None:
        """
        Alias of dump. Dump the current object to a file.

        Args:
            path (QOSSTPath): the path where to save the data.
        """
        return self.dump(path)

    def get_saved_info(self) -> str:
        """
        Get the information on the save (datetime of
        the save, path of the save and if the current
        object was loaded from this path).

        Returns:
            str: string with the save info.
        """
        res = ""
        res += f"Class: {self.__class__.__name__}\n"
        res += f"Path: {self._saved_path}\n"
        res += f"Time of save: {self._saved_datetime}\n"
        res += f"Loaded : {self._loaded}\n"
        return res

    def set_loaded(self) -> None:
        """
        Function to call when the object is loaded.
        """
        self._loaded = True
