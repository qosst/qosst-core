# qosst-core

<center>

![QOSST Logo](qosst_logo_full.png)

</center>

This project is part of [QOSST](https://github.com/qosst/qosst).

## Features

`qosst-core` is the module of QOSST in charge of the common functionalities of Alice and Bob for CV-QKD. In particular it includes:

* Configuration file and reader;
* Authentication;
* Classical communication protocol;
* Modulations;
* Filters and synchronisation sequence for digital signal processing;
* And some utils functions and constant definitions.

## Installation

The module can be installed with the following command:

```console
pip install qosst-core
```

It is also possible to install it directly from the github repository:

```console
pip install git+https://github.com/qosst/qosst-core
```

It also possible to clone the repository before and install it with pip or poetry

```console
git clone https://github.com/qosst/qosst-core
cd qosst-alice
poetry install
pip install .
```

## Documentation

The whole documentation can be found at https://qosst-core.readthedocs.io/en/latest/

## Usage

`qosst-core` will rarely be used as a standalone package. It is worth noting however that there is a command line tool shipped with the `qosst-core` package that has general commands but also the command for authentication initialization and configuration create.

The command line is 

```console
qosst
```

 and more information on it can be found in the CLI section of the documentation.

## License

As for all submodules of QOSST, `qosst-core` is shipped under the [Gnu General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html).

## Contributing

Contribution are more than welcomed, either by reporting issues or proposing merge requests. Please check the contributing section of the [QOSST](https://github.com/qosst/qosst) project fore more information.
