# Control protocol

In the following we described the specifications of the QOSST/0.1 protocol.

## Guidelines to create the client and server

As of CV-QKD, Alice will play the role of server and Bob the role of client.

A strict client-server infrastructure is considered meaning that the server will only answer to requests from the client, and will not send messages by itself.

The client should always send a disconnect message before going down.

The server should do everything possible to not stop. It should only stop in case of a fatal error (unrecoverable configuration error for instance).

## Format of frame

The format of a frame is described below and the one suggested in [https://realpython.com/python-sockets/](https://realpython.com/python-sockets/).

The frame is composed of

1. a fixed length header
2. a signed digest
3. a variable length header
4. a variable length content

The fixed length header is 4 bytes long. The two first bytes should be considered as 2-byte integer following the big endian convention and corresponds to the length of the signed digest. The next 2 bytes of the header should be considered as a 2-byte integer following the big endian convention and corresponds to the length of the variable length header.

The variable length header is a JSON formatted objected containing at least the following information:

* Code of the message (see codes)
* Challenge issued by the other party for the signature
* New unique challenge for the next communication
* Length of the content

If not content is provided in the message. The length of the content should be 0.

The content should be a JSON formatted message. Fields depend on the specific message.

```{figure} ../_static/control-protocol-schema.png
---
align: center
---
Frame structure
```

## Authentication and identification

Codes reserved for Authentication and identification are 100 to 119.

Bob sends an an `IDENTIFICATION_REQUEST` to Alice. This request should contain

* the serial number of Bob;
* the version of the control protocol.

It should also contain the first signature challenge for Alice in the request.

This is the only message Alice should check the signature but not verify a specific challenge.

If the qosst version is compatible, Alice should answer with an `IDENTIFICATION_REQUEST` containing

* the serial number of Alice.

The header should contain Bob's challenge and the next challenge should be using.

From this point Alice and Bob should continue exchanging messages by creating new challenge every time. If for some reason, the flow of challenges is lost at some point, the identification step should be done again.

If the qosst version is not compatible, Alice should answer with an `INVALID_QOSST_VERSION` containing:

* its own control protocol version

Here is the sequence diagram for authentication and identification:

```{figure} ../_static/authentication.png
---
align: center
---
Sequence diagram for authentication
```

Here are the messages (variable length header and content that should be issued):

### IDENTIFICATION_REQUEST

#### Header

```{code-block} JSON
{
  "content_length": 31,
  "code": 100,
  "challenge": "",
  "next_challenge": "some_random_string"
}
```

#### Content

```{code-block} JSON
{
  "serial_number": "QOSST/0002",
  "qosst_version": "QOSST/0.1"
}
```

### IDENTIFICATION_RESPONSE

#### Header

```{code-block} JSON
{
  "content_length": 31,
  "code": 101,
  "challenge": "some_random_string",
  "next_challenge": "another_random_string"
}
```

#### Content

```{code-block} JSON
{
  "serial_number": "QOSST/0001",
}
```

### INVALID_QOSST_VERSION

#### Header

```{code-block} JSON
{
  "content_length": 31,
  "code": 102,
  "challenge": "some_random_string",
  "next_challenge": "another_random_string"
}
```

#### Content

```{code-block} JSON
{
  "qosst_version": "QOSST/0.2",
}
```

## Initialization

Codes reserved for Initialization are 120 to 139.

For each nea frame, Bob has to send an `INITIALIZATION_REQUEST` containing the UUID of the frame, along with optional parameters. Bob is free to put the different parameters he wants, as individual json fields.

Alice should check save the UUID of the frame and check the parameters. If she agrees with the parameters, she send back an `INITIALIZATION_ACCEPTED` response. If she doesn't (several parameters have impossible values for her, or one of the parameters she want to check if missing) she either send back `INITIALIZATION_DENIED` or `INITIALIZATION_PROPOSAL`.

`INITIALIZATION_DENIED` means that Alice denies the parameters and is waiting for Bob to propose new parameters.

`INITIALIZATION_PROPOSAL` means that Alice denies the parameters and is willing to make a configuration proposal. Bob has then the choice to propose other parameters or to ask for the proposal.

In any case, `INITIALIZATION_DENIED` and `INITIALIZATION_PROPOSAL` should contain the `deny_message` field.

Bob can request the configuration proposal by sending the `INITIALIZATION_REQUEST_CONFIG` and Alice should answer with the `INITIALIZATION_CONFIG` with a field containing the config.

Here is the sequence diagram for initialization:

```{figure} ../_static/initialization.png
---
align: center
---
Sequence diagram for initialization
```

### INITIALIZATION_REQUEST

#### Header

```{code-block} JSON
{
  "content_length": 128,
  "code": 120,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "frame_uuid": "9f0b6ea4-9e8c-11ed-8b23-0028f86a9730",
  "optional_parameter": "value",
  "extra_optional_parameter": "other_value"
}
```

### INITIALIZATION_ACCEPTED

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 121,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### INITIALIZATION_DENIED

#### Header

```{code-block} JSON
{
  "content_length": 54,
  "code": 122,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "deny_message": "The roll-off parameter is missing."
}
```


### INITIALIZATION_PROPOSAL

#### Header

```{code-block} JSON
{
  "content_length": 54,
  "code": 123,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "deny_message": "The roll-off parameter is missing."
}
```


### INITIALIZATION_REQUEST_CONFIG

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 124,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

No content.

### INITIALIZATION_CONFIG

#### Header

```{code-block} JSON
{
  "content_length": 1557,
  "code": 125,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "config": "the config object here, in JSON."
}
```

## Quantum Information Exchange

Codes reserved for the Quantum Information Exchange is 140 to 159.

The Quantum Information Exchange (QIE) is one of the most step of CV-QKD.

Bob starts by requesting the start of the QIE with `QIE_REQUEST`. The message should contain the UUID of the frame their are going to work one.

Alice runs her Digital Signal Processing and when the DAC are ready to emit the date, she answers with `QIE_READY`.

Bob launches the acquisition and sends the `QIE_TRIGGER` message.

On receive, Alice trigger the emission and answers with the `QIE_EMISSION_STARTED` message.

When acquisition is done Bob sends `QIE_ACQUISITION_ENDED`.

Alice answers with `QIE_ENDED`.

Here is the diagram sequence for QIE:

```{figure} ../_static/quantum_information_exchange.png
---
align: center
---
Sequence diagram from Quantum Information Exchange
```

### QIE_REQUEST


#### Header

```{code-block} JSON
{
  "content_length": 54,
  "code": 140,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "frame_uuid": "9f0b6ea4-9e8c-11ed-8b23-0028f86a9730",
}
```

### QIE_READY

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 141,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### QIE_TRIGGER

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 142,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

No content.

### QIE_EMISSION_STARTED

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 143,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### QIE_ACQUISITION_ENDED

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 144,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

No content.

### QIE_ENDED

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 145,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

## Parameters estimation

Codes reserved for Parameters Estimation (PE) are 160 to 179.

Bob can request some data from Alice to finish the signal processing and compute the correlations. These points should not be used for the final key. Bob request with the `PE_SYMBOLS_REQUEST` with the list of indices as the content and Alice answers with `PE_SYMBOLS_RESPONSE` with the list of symbols corresponding to these indices as two separate list (one for the real part and one for the imaginary part). If the indices generate an out of bound error, Alice sends back `PE_SYMBOLS_ERROR`.

Bob can then request the number of photon (per symbol) to Alice (remember that 2<n> = Va) with the `PE_NPHOTON_REQUEST` and Alice answers with `PE_NPHOTON_RESPONSE` with the mean number of photon per symbol in the content.

Then Bob sends the `PE_FINISHED` message containing the estimation of the transmittance, the excess noise and the value of key rate. Alice answers back with a `PE_APPROVED` if she wants to continue working on this frame or `PE_DENIED` if not. If the key rate is 0, Alice has to send the `PE_DENIED`.

Here is the sequence diagram:

```{figure} ../_static/parameters_estimation.png
---
align: center
---
Sequence diagram for parameters estimation
```

### PE_SYMBOLS_REQUEST

#### Header

```{code-block} JSON
{
  "content_length": 31,
  "code": 160,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "indices": [1, 57, 17, 90, 3]
}
```

### PE_SYMBOLS_RESPONSE

#### Header

```{code-block} JSON
{
  "content_length": 70,
  "code": 161,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "symbols_real": [1, 1, 1, -1, -1],
  "symbols_imag": [1, -1, 1, 1, -1]
}
```

### PE_SYMBOLS_ERROR

#### Header

```{code-block} JSON
{
  "content_length": 73,
  "code": 162,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "error_message": "Indice 10000 is out of bound for array of size 5000."
}
```

### PE_NPHOTON_REQUEST

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 163,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

No content.

### PE_NPHOTON_RESPONSE

#### Header

```{code-block} JSON
{
  "content_length": 18,
  "code": 164,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "n_photon": 1.54
}
```

### PE_FINISHED

#### Header

```{code-block} JSON
{
  "content_length": 116,
  "code": 165,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "n_photon": 1.54,
  "transmittance": 0.5,
  "excess_noise": 0.1,
  "electronic_noise": 0.05,
  "eta": 0.8,
  "key_rate": 200
}
```

### PE_APPROVED

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 166,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### PE_DENIED

#### Header

```{code-block} JSON
{
  "content_length": 37,
  "code": 167,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "deny_message": "Key rate is null."
}
```

## Error correction

Codes reserved for Error Correction (EC) are 180 to 199.

Bob sends a `EC_INITIALIZATION` with the parameters required for the error correction step. Alice can accept with `EC_READY` or `EC_DENIED`. Alice and Bob will then loop to correct every block with Bob first sending a `EC_BLOCK` and Alice responding `EC_BLOCK_ACK` if the correction worked or `EC_BLOCK_ERROR` if not.

At the end of this loop, there might still have some remaining errors and Bob can start another algorithm for correcting those errors with `EC_REMAINING`. Alice answers either with `EC_REMAINING_ACK` if it was successful or `EC_REMAINING_ERROR` if it was not.

At the end, Bob computes the hash of his key and send to Alice with the messages `EC_VERIFICATION`. If the hashes are equal, Alice answers with `EC_VERIFICATION_SUCCESS`, and if not `EC_VERIFICATION_FAIL`.


Here is the sequence diagram:

```{figure} ../_static/error_correction.png
---
align: center
---
Sequence diagram for error correction
```

```{warning}
This part will probably change as the error correction algorithm is still not very defined.
```

### EC_INITIALIZATION

#### Header

```{code-block} JSON
{
  "content_length": 42,
  "code": 180,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "matrix": [[1,1], [1,1]],
  "noise": 0.1,
}
```

### EC_READY

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 181,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### EC_DENIED

#### Header

```{code-block} JSON
{
  "content_length": 41,
  "code": 182,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "error_message": "Matrix is not valid."
}
```

### EC_BLOCK

#### Header

```{code-block} JSON
{
  "content_length": 26,
  "code": 183,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "syndrome": [1.87, 5.67,]
}
```

### EC_BLOCK_ACK

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 184,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### EC_BLOCK_ERROR

#### Header

```{code-block} JSON
{
  "content_length": 43,
  "code": 185,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "error_message": "Wrong syndrome length."
}
```

### EC_REMAINING

#### Header

```{code-block} JSON
{
  "content_length": 21,
  "code": 186,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "some_parameter": 1,
}
```

### EC_REMAINING_ACK

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 187,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### EC_REMAINING_ERROR

#### Header

```{code-block} JSON
{
  "content_length": 37,
  "code": 188,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "error_message": "Wrong parameter."
}
```

### EC_VERIFICATION

#### Header

```{code-block} JSON
{
  "content_length": 28,
  "code": 189,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "hash": 385789897481570657,
}
```

### EC_VERIFICATION_SUCCESS

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 190,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### EC_VERIFICATION_FAIL

#### Header

```{code-block} JSON
{
  "content_length": 40,
  "code": 191,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "error_message": "Keys are not equal."
}
```

## Privacy amplification

Codes reserved for Parameters Estimation (PA) are 200 to 219.

For Privacy Amplification, Bob request it by sending the `PA_REQUEST` along with the parameter needed to perform the privacy amplification.  Alice answers with `PA_SUCCESS` if the privacy amplification was done successfully and `PA_ERROR` if there was an error.

Here is the sequence diagram:

```{figure} ../_static/privacy_amplification.png
---
align: center
---
Sequence diagram for privacy amplification
```

### PA_REQUEST

#### Header

```{code-block} JSON
{
  "content_length": 114,
  "code": 200,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "seed": [1,0,1,1,0],
  "secret_key_length": 2000,
  "subblock_length": 5,
  "feedback_polynomial": [1,1,1,0,0],
}
```

### PA_SUCCESS

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 201,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### PA_ERROR

#### Header

```{code-block} JSON
{
  "content_length": 63,
  "code": 202,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "error_message": "Invalid value for the feedback polynomial."
}
```

## End of frame

Codes reserved for end of frame and end of communication are 220 to 229.

After privacy amplification, Bob confirms the end on working on a frame by sending the `FRAME_ENDED`, with the UUID of the frame as content and Alice answers with the `FRAME_ENDED_ACK` also with the UUID of the frame.

Here the sequence diagram:

```{figure} ../_static/end_of_frame.png
---
align: center
---
Sequence diagram for end of frame
```

### FRAME_ENDED

#### Header

```{code-block} JSON
{
  "content_length": 54,
  "code": 220,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "frame_uuid": "9f0b6ea4-9e8c-11ed-8b23-0028f86a9730",
}
```

### FRAME_ENDED_ACK

#### Header

```{code-block} JSON
{
  "content_length": 54,
  "code": 221,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "frame_uuid": "9f0b6ea4-9e8c-11ed-8b23-0028f86a9730",
}
```

## End of communication

Codes reserved for end of frame and end of communication are 220 to 229.

The graceful disconnection of the client is Bob sending `DISCONNECTION` and Alice answering with `DISCONNECTION_ACK`.

Here is the sequence diagram

```{figure} ../_static/end_of_communication.png
---
align: center
---
Sequence diagram for end of communication
```

### DISCONNECTION

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 222,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

No content.

### DISCONNECTION_ACK

#### Header

```{code-block} JSON
{
  "content_length": 54,
  "code": 223,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

## Parameter change

Codes 50 to 69 are reserved for parameter change.

When Bob wants Alice to change a parameter, Bob sends a `CHANGE_PARAMETER_REQUEST` with the name of the parameter and the requested value in the content.

Alice has then four possible answers:

* `PARAMETER_CHANGED`: she has accepted the change. The name of the parameter, the old value and the new value should be in the content.
* `PARAMETER_UNKOWN`: Alice didn't find the parameter. The name of the parameter should be in the content.
* `PARAMETER_INVALID_VALUE`: Alice found the parameter, but the requested value either makes no sense for this parameter or is out of the possible range for Alice. The name of the parameter and the old value should be in the content. An error message can also be in the content to give more information on the non-validity of the value.
* `PARAMETER_UNCHANGED`: Alice found the parameter and the value is a valid value. However, due to policy, Alice didn't change the value of the parameter. The name of the parameter and the old value should be in the content. An error message giving more information can also be added.

Here is the diagram sequence for the parameter change:

```{figure} ../_static/parameter_change.png
---
align: center
---
Sequence diagram for parameter change
```

### CHANGE_PARAMETER_REQUEST

#### Header

```{code-block} JSON
{
  "content_length": 48,
  "code": 50,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "parameter": "qi.frame.roll_off",
  "value": 0.3
}
```

### PARAMETER_CHANGED

#### Header

```{code-block} JSON
{
  "content_length": 70,
  "code": 51,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "parameter": "qi.frame.roll_off",
  "old_value": 0.5,
  "new_value": 0.3
}
```

### PARAMETER_UNKOWN

#### Header

```{code-block} JSON
{
  "content_length": 34,
  "code": 52,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "parameter": "qi.frame.roll_olf",
}
```

### PARAMETER_INVALID_VALUE

#### Header

```{code-block} JSON
{
  "content_length": 52,
  "code": 53,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "parameter": "qi.frame.roll_off",
  "old_value": 0.5,
}
```

### PARAMETER_UNCHANGED

#### Header

```{code-block} JSON
{
  "content_length": 52,
  "code": 54,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "parameter": "qi.frame.roll_off",
  "old_value": 0.5,
}
```

## Polarisation recovery

Codes 70 to 79 are reserved for polarisation recovery.

When Bob wants to start the polarisation recovery, he sends `REQUEST_POLARISATION_RECOVERY`, and Alice should start the emission of the classical signal and respond with `POLARISATION_RECOVERY_ACK`. Bob should then perform the polarisation recovery algorithm and when done, send the `END_POLARISATION_RECOVERY` and Alice should stop the classical signal and respond `POLARISATION_RECOVERY_ENDED`.

Here is the diagram sequence for the polarisation recovery:

```{figure} ../_static/polarisation_recovery.png
---
align: center
---
Sequence diagram for parameter change
```

### REQUEST_POLARISATION_RECOVERY

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 70,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### POLARISATION_RECOVERY_ACK

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 71,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### END_POLARISATION_RECOVERY

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 72,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### POLARISATION_RECOVERY_ENDED

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 73,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

## Other messages

The codes reserved for this other messages is 10-49.

### UNKNOWN_COMMAND

Alice should answer with an `UNKOWN_COMMAND` if the provided command was unknown (i.e. is not a command in the description of the protocol). It should return the code that was issued.

#### Header

```{code-block} JSON
{
  "content_length": 14,
  "code": 10,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "code": 1000
}
```

### UNEXPECTED_COMMAND

Alice should answer an `UNEXPECTED_COMMAND` if the command asked by Bob exist but doesn't make sense in the current context. The code of the required command should be provided. An optional error message can also be issued.

#### HEADER

```{code-block} JSON
{
  "content_length": 14,
  "code": 11,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "code": 200,
  "error_message": "Privacy amplification cannot be donne before error correction."
}
```

### INVALID_CONTENT

Alice should answer `INVALID_CONTENT` if the content in the request is not valid valid according to the current specification. The code of the requested command should be given, along with an optional error message.

#### Header

```{code-block} JSON
{
  "content_length": 14,
  "code": 12,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

```{code-block} JSON
{
  "code": 200,
  "error_message": "Seed parameter was not present in the content."
}
```

### INVALID_RESPONSE

If Bob receives an invalid response to one of its request (the code is not part of the ones he expect, or the content was malformed), he sends to Alice an `INVALID_RESPONSE`. An optional error_message can be passed. Alice should respond with an `INVALID_RESPONSE_ACK`. After that, Bob will probably have to disconnect.

#### Header

```{code-block} JSON
{
  "content_length": 60,
  "code": 13,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "error_message": "Code 221 made no sense in this context."
}
```

### INVALID_RESPONSE_ACK

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 14,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### ABORT

If at any point Bob wants to abort the current frame, he sends an `ABORT` message. The message can contain an optional message to explain decision. Alice should answer with an `ABORT_ACK`.

This doesn't mean that Bob is going down. If he wants to end the communication gracefully, he stills need an `DISCONNECTION` message. However, it means that all the work on the current frame should be deleted.

If Alice wants to abort, she answered to any Bob message with `ABORT` and Bob should abort immediately.

#### Header

```{code-block} JSON
{
  "content_length": 40,
  "code": 15,
  "challenge": "challenge_requested_by_alice",
  "next_challenge": "next_challenge_for_alice"
}
```

#### Content

```{code-block} JSON
{
  "abort_message": "Physical tempering."
}
```

### ABORT_ACK

Alice answers back to Bob with `ABORT_ACK` when she receives an `ABORT` message.

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 16,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

### AUTHENTICATION_INVALID

If at some point Bob notices an invalid authentication from Alice, he do again the authentication part (after a specific amount of failure, Bob concludes to a man in the middle attack).

If Alice notices an invalid authentication with one of Bob's message, she sends `AUTHENTICATION_INVALID` and Bob should do again the authentication part. After a certain number of authentication failures, Alice concludes to a man in the middle attack.

#### Header

```{code-block} JSON
{
  "content_length": 0,
  "code": 17,
  "challenge": "challenge_requested_by_bob",
  "next_challenge": "next_challenge_for_bob"
}
```

#### Content

No content.

## Error codes

Low layers can return error codes that are directly communication codes. They indicate to higher application layers that something went wrong when receiving the frame but it doesn't raise an exception.

The error codes are:

 * `SOCKET_DISCONNECTION = -1`: other party has disconnected;
 * `FRAME_ERROR = -2`: there was an error reading the frame (non valid JSON, missing header value, frame too short);
 * `AUTHENTICATION_FAILURE = -3`: there was an error while verifying the integrity and/or the authentication of the message;
 * `UNKOWN_CODE = -4`: the given code is not a valid QOSST code.


## Full sequence diagram

The full sequence diagram is given below:

```{figure} ../_static/all.png
---
align: center
---
Full sequence diagram
```

## List of codes

```{eval-rst}
.. automodule:: qosst_core.control_protocol.codes
    :members:
    :undoc-members:
    :member-order: bysource
    :noindex:
```
