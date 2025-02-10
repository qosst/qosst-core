"""
Function to show the different dependencies and let the user print their license.
"""

from typing import Dict
from pathlib import Path

DEPS: Dict[str, str] = {
    "numpy": "custom",
    "scipy": 'BSD 3-Clause "New" or "Revised" License',
    "matplotlib": "custom",
    "FreeSimpleGUI": "GNU Lesser General Public License v3.0",
    "python": "Python Software Foundation License Version 2",
    "qosst": "GNU General Public License v3.0",
    "falcon-digital-signature": "MIT License",
    "toml": "MIT License",
    "requests": "Apache License 2.0",
    "importlib-metadata": "Apache License 2.0",
    "IR_for_CVQKD": "GNU General Public License v3.0",
    "cryptomite": "custom",
}


def list_licenses() -> bool:
    """List dependencies and let the user print their license.

    Returns:
        bool: True in case of a sucessful operation, False otherwise.
    """
    licenses_path = Path(__file__).parent

    text = ""
    i = 0
    keys = []
    for key, val in DEPS.items():
        text += f"[{i}] {key} - {val}\n"
        keys.append(key)
        i += 1

    while True:
        print(text)
        user_input = input(f"Choose a license to show [0-{i-1}] or E to exit. ")
        if user_input == "E":
            return True
        try:
            choice = int(user_input)
        except ValueError:
            print(f"{user_input} is not valid integer.")
            continue

        if choice < 0 or choice > i - 1:
            print(f"{user_input} is outside the range of valid licenses choice.")

        dep = keys[choice]
        print(f"Displaying license for {dep}")

        with open(licenses_path / f"{dep}.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                print(line, end="")

        print("\n\n")

        cont = input("Press E to exit or any other key to continue. ")
        if cont == "E":
            return True


if __name__ == "__main__":
    list_licenses()
