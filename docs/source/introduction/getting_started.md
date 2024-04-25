# Getting started

## Hardware requirements

### Operating System

The QOSST suite does not required a particular software and should work on Windows (tested), Linux (tested) and Mac (not tested).

The actual operating system requirement will come down to the hardware used for the experiment since some of them don't have interfaces with Linux.

### Python version

QOSST if officially supporting any python version 3.9 or above.

## Installing the software

There are several ways of installing the software, either by using the PyPi repositories or using the source.

```{note}
You usually don't have to install the qosst-core package manually as it shipped with qosst-alice and qosst-bob. If you however need it, the installation are given below.
```

### Installing the qosst-core package

To install the `qosst-core` package.

```{prompt} bash

pip install qosst-core
```

Alternatively, you can clone the repository at [https://github.com/qosst/qosst-core](https://github.com/qosst/qosst-core) and install it by source.

## Checking the version of the software

`qosst-core` provides the `qosst` command from which the whole documentation can be found [here](../cli/documentation.md).

You can check the version by issuing the command

```{command-output} qosst info
```

If the `qosst` command was not installed in the path, it also possible to run the following command:

```{prompt} bash
python3 -m qosst_core.commands info
```

or

```{prompt} bash
python3 -c "from qosst_core.infos import get_script_infos; print(get_script_infos())"
```

In the following we will assume that you have access to the qosst (and other) commands. If not you can replace the instructions similarly to above.

If this works and have the latest version, you should be ready to go !