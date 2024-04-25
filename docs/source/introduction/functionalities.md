# Functionalities

The `qosst-core` package provides the core functionalities that are required by both Alice and Bob. In particular, it implements:

* [configuration module](../understanding/configuration.md);
* [control protocol](../understanding/control_protocol.md) for the classical channel;
* [authentication module](../understanding/authentication.md);
* [modulation and constellations](../understanding/modulation.md);
* [communication functions](../understanding/comm.md): filters and Zadoff-Chu sequence;
* [data containers](../understanding/data.md);
* [notifications](../understanding/notifications.md);
* some utils functions.

A rapid overview is given below but the full documentation should be consulted for more information.

## Configuration

The configuration module contains the different classes that will load the configuration from a TOML file and hold the configuration to be later used in the script.

For instance, a part of the configuration file looks like the following:

```{code-block} toml
[frame]
[frame.quantum]

# Number of symbols for the quantum part
# Default : 1000000
num_symbols = 1000000
```

and then if the configuration is loaded through the {py:class}`Configuration <qosst_core.configuration.configuration.Configuration>` class, the data can be accessed as such:

```{code-block} python

from qosst_core.configuration import Configuration

config = Configuration("configuration/config.example.toml")

config.frame.quantum.num_symbols # 100000
```

More information on the configuration can be found [here](../understanding/configuration.md)

## Control protocol

The control protocol defines the network protocol that is used on the classical channel to communicate between Alice and Bob. In particular this modules defines the protocol, the communication codes and helper classes for the communication.

### Overview of the control protocol

The frame that is exchanged for each message of the network protocol is described on the following schema:

```{figure} ../_static/control-protocol-schema.png
---
align: center
---
Frame structure
```

It is composed of a

1. a fixed length header of 4 bytes containing the length of the signed digest;
2. the signed digest for authentication (see the next section);
3. a variable length header containing the code of the message and the length of the content;
4. the content.

The most important piece of information is the code of the message the encodes most of the meaning. The content is optional and depends on the code of the message.

The code of the message is an integer between 0 and 255 and encodes the meaning of the message. For instance, the message "start the emission of the data" corresponds to the code 142. The list of codes can be found in {py:class}`QOSSTCodes <qosst_core.control_protocol.codes.QOSSTCodes>`.

The diagram sequences of the protocol can be found [here](../understanding/control_protocol.md).

### Helper classes

The module also implements helper classes (call sockets), and in particular a client socket and a server socket. Messages can be sent easily by taking the code and the content as parameter and received easily by returning the code and the content. The authentication and the buffers are handled by this classes and is transparent for the higher users. It also handles properly the disconnection.

Here is a minimal example of how these classes could be used:

```{code-block} python
from qosst_core.control_protocol.sockets import QOSSTServer

server = QOSSTServer("127.0.0.1", 8181) # Listening address and port
server.open()
server.connect() # Waits until client connects

code, data = server.recv() # code = QOSSTCodes.QIE_TRIGGER, data = None

server.close()
```

```{code-block} python
from qosst_core.control_protocol.sockets import QOSSTClient
from qosst_core.control_protocol.codes import QOSSTCodes

client = QOSSTClient("127.0.0.1", 8181) # Server address and port
client.open()
client.connect() # Server needs to be waiting here

client.send(QOSSTCodes.QIE_TRIGGER)

client.close()
```

## Authentication

Authentication is a crucial requirement for any QKD protocol with a classical channel. In our case, this is handle with a signed digest. For each message a digest of the variable length header and the data needs to computed and then signed before being added between the fixed length header and the variable length header. As some messages are similar, each party has to include a challenge response and challenge request in the variable length header. This is example in more details [here](../understanding/authentication.md).

The digest is computed using the SHA256 algorithm and two signatures scheme currently exist in the `qosst-core` package:

* no signature: the signed digest is the digest and the verification is only to verify that both digests are equal.
* falcon: the digest is signed using the asymmetric algorithm [falcon](https://falcon-sign.info/) which is one of the finalist as a post-quantum cryptographic protocol.

## Modulations

In CV-QKD, Alice draws random symbols according to a distribution. This distribution can be either continuous or discrete.

This module implements 6 modulation formats and the code to draw symbols from those modulation formats.

Here is a short description of the 6 modulations formats:

* [Gaussian](../understanding/modulation.md#gaussian): both the real and imaginary part of the symbols are generated using a Gaussian distribution with mean 0 and a user defined variance.
* [Phase Shift Keying (PSK)](../understanding/modulation.md#phase-shift-keying-psk): all the symbols are placed on a circle, and are equally spaced. The number of symbols is called the size of the modulation and should be a power of 2. All the symbols are equally probable. The size of the circle depends on the variance selected by the user.
* [Quadrature Amplitude Modulation (QAM)](../understanding/modulation.md#quadrature-amplitude-modulation-qam): all the symbols are placed on a grid, and are equally spaced. The number of symbols is called the size of the modulation and should be a power of 2 and a perfect square. All the symbols are equally probable. The size of the grid depends on the variance selected by the user.
* [Probabilistic Constellation Shaping Quadrature Amplitude Modulation (PCS-QAM)](../understanding/modulation.md#probabilistic-constellation-shaping-qam-pcs-qam): this is a QAM where the probabilities are changed to approximate a Gaussian distribution.
* [Binomial Quadrature Amplitude Modulation (Binomial-QAM)](../understanding/modulation.md#binomial-quadrature-amplitude-modulation-binomial-qam): this is a QAM where the probabilities are changed to approximate a Gaussian distribution.
* [Single Point Modulation](../understanding/modulation.md#single-point): this is a test modulation with a single point.

Here is an example of how to use the modulation classes:

```{code-block} python

from qosst_core.modulation import PSKModulation

modulation = PSKModulation(1, 4) # 1 for the variance, 4 for the size i.e. 4-PSK (or QPSK)
points = modulation.modulate(1000) # Generate 1000 random symbols from this modulation
```

## Communication

The communication (`comm`) module is a very important one since it provides the synchronisation sequence and the filters.

More information can be found [here](../understanding/comm.md).

### Filters

The module provides raised cosine, root raised cosine and square filters, that can be use to shape the symbols at Alice side.

### Zadoff-Chu sequence

The Zadoff-Chu sequence is used for synchronisation since it has good autocorrelations properties: it's a Constant Amplitude Zero AutoCorrelation (CAZAC) sequence.

## Data

Data containers are classes that inherits from the {py:class}`BaseQOSSTData <qosst_core.data.BaseQOSSTData>` class that offers ways to easily export and load the data.

For instance a data container for an array of excess noises and transmittances could be represented and used in the following way:

```{code-block} python

import numpy as np
from qosst_core.data import BaseQOSSTData

class Result(BaseQOSSTData):
    excess_noises: np.ndarray
    transmittances: np.ndarray

    def __init__(self, excess_noises: np.ndarray, transmittances: np.ndarray):
        self.excess_noises = excess_noises
        self.transmittances = transmittances


result = Result(np.array([0.01]), np.array([0.5]))
result.save("my_result.qosst")

result2 = Result.load("my_result.qosst")

```

More information is available [here](../understanding/data.md).

## Notifications

The notification module implements notifiers to send messages at the end of experiments. It can sometimes be useful for repeated experiment.

The notifiers implement a `send_notification` function, that will use the parameters passed during init to send the notification.

More information is available [here](../understanding/notifications.md).

## Utils

The utils module contains some functions that are useful:

* {py:func}`eph <qosst_core.utils.eph>`: computes the energy of a photon given its wavelength;
* {py:func}`decimal_to_bitarray <qosst_core.utils.decimal_to_bitarray>` and {py:func}`bitarray_to_decimal <qosst_core.utils.bitarray_to_decimal>`: conversion between array of bits and integers;
* {py:func}`generate_gray <qosst_core.utils.generate_gray>`: generates a Gray code;
* {py:func}`export_np <qosst_core.utils.export_np>`: shortcut to save data and metadata (better to use data containers);
* {py:func}`get_object_by_import_path <qosst_core.utils.get_object_by_import_path>`: return a python object by its import path;
* {py:func}`round <qosst_core.utils.round>`: round a float by always rounding in the same way;
* {py:func}`configuration_menu <qosst_core.utils.configuration_menu>`: print a configuration menu for a configuration class for some tools.

In the next section we will provide in-depth explanation of each module.
