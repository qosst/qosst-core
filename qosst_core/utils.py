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
Utils module for qosst-core.
"""
from typing import Tuple, List, Union, Any, Optional
from os import PathLike
import functools
from pathlib import Path
from datetime import datetime
from dataclasses import is_dataclass, fields

import toml
from scipy import constants as c
import numpy as np

# Define custom types here
QOSSTPath = Union[str, PathLike[str]]


def eph(lamb: float) -> float:
    """
    Returns the energy of a single photon
    of wavelength lamb.

    Args:
        lamb (float): wavelength in meter.

    Returns:
        float: energy of photon.
    """
    return c.h * c.c / lamb


def decimal_to_bitarray(in_number: np.ndarray, bit_width: int) -> np.ndarray:
    """
    Converts a positive integer or an array-like of positive integers to NumPy array of the specified size containing
    bits (0 and 1).

    Args:
        in_number (int or array-like of int): Positive integer to be converted to a bit array.
        bit_width (int): Size of the output bit array.

    Returns:
        np.ndarray: Array containing the binary representation of all the input decimal(s).
    """

    if isinstance(in_number, (np.integer, int)):
        return _decimal_to_bitarray(in_number, bit_width).copy()
    result = np.zeros(bit_width * len(in_number), np.int8)
    for pox, number in enumerate(in_number):
        result[pox * bit_width : (pox + 1) * bit_width] = _decimal_to_bitarray(
            number, bit_width
        ).copy()
    return result


@functools.lru_cache(maxsize=128, typed=False)
def _decimal_to_bitarray(number: int, bit_width: int) -> np.ndarray:
    """
    Converts a positive integer to NumPy array of the specified size containing bits (0 and 1). This version is slightly
    quicker that dec2bitarray but only work for one integer.

    Args:
        in_number (int): Positive integer to be converted to a bit array.
        bit_width (int): Size of the output bit array.

    Returns:
        np.ndarray: Array containing the binary representation of all the input decimal(s).
    """
    result = np.zeros(bit_width, np.int8)
    i = 1
    pox = 0
    while i <= number:
        if i & number:
            result[bit_width - pox - 1] = 1
        i <<= 1
        pox += 1
    return result


def bitarray_to_decimal(in_bitarray: np.ndarray) -> int:
    """
    Converts an input NumPy array of bits (0 and 1) to a decimal integer.

    Args:
        in_bitarray (np.ndarray): Input NumPy array of bits.

    Returns:
        int: Integer representation of input bit array.
    """

    number = 0

    for i, val in enumerate(in_bitarray):
        number = number + val * pow(2, len(in_bitarray) - 1 - i)

    return number


def generate_gray(number_bits: int) -> List[str]:
    """
    Generate a Gray code with number_bits bits.

    The result is returned as list of strings.

    Args:
        number_bits (int): number of bits in the code

    Returns:
        List[str]: Gray code as a list of strings.
    """
    if number_bits <= 0:
        return ["0"]
    if number_bits == 1:
        return ["0", "1"]
    rec_ans = generate_gray(number_bits - 1)
    ans = []
    for val in rec_ans:
        ans.append("0" + val)

    for i in range(len(rec_ans) - 1, -1, -1):
        ans.append("1" + rec_ans[i])

    return ans


def export_np(
    data: np.ndarray,
    export_dir: QOSSTPath,
    metadata: Optional[np.ndarray] = None,
    data_name: str = "data",
    metadata_name: str = "metadata",
) -> Tuple[Optional[QOSSTPath], Optional[QOSSTPath]]:
    """
    Save the data in metada in the export_dir directory with a timestamp.

    Args:
        data (np.ndarray): data array to save.
        export_dir (QOSSTPath): where to save the data and metadata.
        metadata (np.ndarray, optional): metadata array to save. Defaults to None.
        data_name (str, optional): the prefix of the saved data array. Defaults to "data".
        metadata_name (str, optional): the prefix of the save metadata array. Defaults to "metadata".

    Returns:
        Tuple[Optional[QOSSTPath], Optional[QOSSTPath]]: tuple containing the path(s) of the saved objects.
    """
    # Verify if dir exists
    # If dir doesn't exist, try to create it
    path = Path(export_dir)
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    # Generate the filename
    filename = path / f"{data_name}-{now:%Y-%m-%d_%H-%M-%S}"

    # If metadata is given, generate the filename for metadata
    metadata_filename: QOSSTPath = ""
    if metadata:
        metadata_filename = path / f"{metadata_name}-{now:%Y-%m-%d_%H-%M-%S}"

    if path.is_dir():
        # Save the data
        np.save(filename, data)

        # If metadata is given, save metadata
        if metadata:
            np.save(metadata_filename, metadata)

        return (filename, metadata_filename)
    return (None, None)


def get_object_by_import_path(import_path: str) -> Any:
    """
    Get an object from it's full import path.

    For instance you get the class NoneAuthenticator with

    get_object_by_import_path("qosst_core.authentication.base.NoneAuthenticator")

    It is also possible to get functions or any other python objects.

    Args:
        import_path (str): the full import path.

    Raises:
        ImportError: the module was not found.
        ImportError: the object was not found in the module.

    Returns:
        object: the object of the full import path.
    """
    module_name = ".".join(import_path.split(".")[:-1])
    class_name = import_path.split(".")[-1]
    if not module_name:
        raise ImportError(f"Impossible to load the object {import_path}")
    try:
        module = __import__(module_name, fromlist=[class_name])
    except ImportError as exc:
        raise ImportError(f"Impossible to load the object {import_path}") from exc

    return getattr(module, class_name)


# pylint: disable=redefined-builtin
def round(input: Union[float, np.ndarray]) -> Union[int, np.ndarray]:
    """
    Round the floats using the ceil(x-0.5) method, that will always round
    in the same direction, especially in the 0.5 case

    For instance
    round(2.4) = 2
    np.round(2.7) = 3

    round(2.5) = 2
    np.round(2.5) = 2

    but
    round(3.5) = 3
    np.round(3.5) = 4

    (in np.round, odd int + 0.5 are rounded to int+1 where even int + 0.5 are rounded to int).

    This method will always round down.


    Args:
        x (Union[float, np.ndarray]): the float or the array of floats to round.

    Returns:
        Union[int, np.ndarray]: the rounded int or the array of rounded ints.
    """
    return np.ceil(input - 0.5).astype(int)


def configuration_menu(
    config: Any, preferred_config_name: Optional[str] = None
) -> None:
    """New configuration menu that uses by default configuration files.

    Args:
        config (Any): configuration object, instance of dataclass.
        preferred_config_name (Optional[str], optional): name, without the .toml extension, of the preferred confiugration to use. Defaults to None.

    Raises:
        TypeError: if the configuration file cannot be read.
    """
    if not is_dataclass(config.__class__):
        raise TypeError(
            "The configuration menu can only be applied to instance of dataclasses."
        )
    print("Welcome to the new configuration menu !")

    # First list all toml configuration file in the current directory.
    current_dir = Path.cwd()
    configuration_files = list(current_dir.glob("*.toml"))
    configuration_filenames = [file.stem for file in configuration_files]
    if configuration_files:
        if preferred_config_name in configuration_filenames:
            decision = input(
                f"Good news ! The preferred configuration {preferred_config_name}.toml has been found in the current directory. Use {preferred_config_name}.toml ? [Y/n] "
            )
            # Yes is the default value
            if decision.lower() == "y" or decision == "":
                load_config_from_file(
                    config,
                    configuration_path=str(
                        configuration_files[
                            configuration_filenames.index(preferred_config_name)
                        ]
                    ),
                )
                return
        print(
            "Preferred configuration file not found or not used. Here are the possible configuration files to use:"
        )
        for i, filename in enumerate(configuration_filenames):
            print(f"[{i}] {filename}")
        print("\n")
        choice = input(
            f"Select a configuration file to use [0...{len(configuration_filenames)-1}]. Leave blank to use the legacy configuration menu: "
        )
        if choice:
            load_config_from_file(
                config, configuration_path=configuration_files[int(choice)]
            )
        else:
            legacy_configuration_menu(config)
    else:
        legacy_configuration_menu(config)


def load_config_from_file(config: Any, configuration_path: Union[Path, str]):
    """Load the config dataclass from the configuration file.

    Args:
        config (Any): config object, instance of dataclass.
        configuration_path (str): path of the configuration file to load the fields data from.
    """
    class_fields = fields(config.__class__)
    try:
        loaded_config = toml.load(configuration_path)
        for class_field in class_fields:
            if class_field.name in loaded_config:
                field_name = class_field.name
                new_value = loaded_config[field_name]
                setattr(
                    config,
                    field_name,
                    type(getattr(config, field_name))(new_value),
                )
    except toml.TomlDecodeError as exc:
        print(
            f"The configuration at path {configuration_path} is not valid (exception: {exc}). Please provide a valid configuation path."
        )


def legacy_configuration_menu(config: Any):
    """
    Print a configuration menu for dynamic configuration modification.

    Args:
        config (Any): the configuration object to change. It as to be an instance of a dataclass.
    """
    if not is_dataclass(config.__class__):
        raise TypeError(
            "The configuration menu can only be applied to instance of dataclasses."
        )
    print("Welcome to the menu to change configuration")
    action = None
    class_fields = fields(config.__class__)
    while action != "E":
        print("Here are the fields you can change:")
        for i, class_field in enumerate(class_fields):
            print(f"[{i}] {class_field.name}")

        print(
            "\nYou can select a field to change with the field number, load a toml configuration file with L, print the configuration with P and Exit with the current configuration with E.\n"
        )
        action = input(
            f"Select your action: [{'/'.join([str(i) for i in range(len(class_fields))])}/P/E] "
        )
        if action in [str(i) for i in range(len(class_fields))]:
            field_name = class_fields[int(action)].name
            print(f"\nCurent value for {field_name}: {getattr(config, field_name)}")
            new_value = input(f"Set new value for field {field_name}: ")
            # We have to use the same type for the new value
            setattr(config, field_name, type(getattr(config, field_name))(new_value))

            print(f"{new_value} has been set for {field_name}\n")
        if action == "P":
            print("\n")
            print(config)
            second_action = input("Continue changing parameter [Y/n] ")
            if second_action == "n":
                action = "E"
