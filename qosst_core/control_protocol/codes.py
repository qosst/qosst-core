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
Enumeration of the QOSST/0.2 protocol.
"""

from enum import IntEnum


class QOSSTCodes(IntEnum):
    """
    Codes for the QOSST/0.2 protocol.
    """

    # Generic codes (10-49)
    UNKOWN_COMMAND = 10  #: Code for an unkown command.
    UNEXPECTED_COMMAND = 11  #: Code for an unexpected command.
    INVALID_CONTENT = 12  #: Code indicating that the content was invalid.
    INVALID_RESPONSE = 13  #: Code indcating an invalid response.
    INVALID_RESPONSE_ACK = 14  #: Code to acknowledge an invalid reponse message.
    ABORT = 15  #: Abort code.
    ABORT_ACK = 16  #: Acknowledge an abortion code.
    AUTHENTICATION_INVALID = 17  #: Indicate that an authentication message was invalid.

    # Parameter change (50-69)
    CHANGE_PARAMETER_REQUEST = 50  #: Code to request a change of parameter.
    PARAMETER_CHANGED = (
        51  #: Code to answer to a parameter change request with confirmation of change.
    )
    PARAMETER_UNKOWN = (
        52  #: Code to answer to a parameter change request if the parameter is unknown.
    )
    PARAMETER_INVALID_VALUE = 53  #: Code to answer to a parameter change request if the requested value is invalid.
    PARAMETER_UNCHANGED = 54  #: Code to answer to a parameter change request saying that the parameter was not changed.

    # Polarisation recovery (70-79)
    REQUEST_POLARISATION_RECOVERY = (
        70  #: Code to ask for the emission of the sequence for polarisation recovery.
    )
    POLARISATION_RECOVERY_ACK = (
        71  #: ACK after enabling the sequence for polarisation recovery.
    )
    END_POLARISATION_RECOVERY = (
        72  #: Code to ask for the stop of the sequence for polarisation recovery.
    )
    POLARISATION_RECOVERY_ENDED = (
        73  #: ACK after stopping the sequence for polarisation recovery.
    )

    # Reserved (80-99)

    # Authentication and Identification (100-119)
    IDENTIFICATION_REQUEST = 100  #: Request the start of the identification process.
    IDENTIFICATION_RESPONSE = 101  #: Response to a request of identification.
    INVALID_QOSST_VERSION = 102  #: Response to answer to an identification request if the versions of the QOSST protocols are not compatible.

    # Initialization (120-139)
    INITIALIZATION_REQUEST = 120  #: Request the start of the initialization process.
    INITIALIZATION_ACCEPTED = 121  #: Accept the initialization (i.e. configuration).
    INITIALIZATION_DENIED = 122  #: Deny the initialization (i.e. configuration).
    INITIALIZATION_PROPOSAL = 123  #: Propose a configuration.
    INITIALIZATION_REQUEST_CONFIG = 124  #: Request a configuration.
    INITIALIZATION_CONFIG = 125  #: Send the configuration for the initialization.

    # Quantum Information Exchange (140-159)
    QIE_REQUEST = 140  #: Request the start of the Quantum Information Exchange process.
    QIE_READY = 141  #: Notify that the quantum information is ready to be sent.
    QIE_TRIGGER = 142  #: Start the quantum information exchange.
    QIE_EMISSION_STARTED = 143  #: Notify that the emission has started.
    QIE_ACQUISITION_ENDED = 144  #: Notify that the acquisition has ended.
    QIE_ENDED = 145  #: End the QIE process.

    # Parameters Estimation (160-179)
    PE_SYMBOLS_REQUEST = 160  #: Request some symbols to Alice.
    PE_SYMBOLS_RESPONSE = 161  #: Answer to the request of symbols.
    PE_SYMBOLS_ERROR = 162  #: Answer to the request of symbols if there was an error to to generate the response (i.e. invalid indices).
    PE_NPHOTON_REQUEST = 163  #: Request the average photon number of Alice.
    PE_NPHOTON_RESPONSE = 164  #: Response to the request of the average photon number.
    PE_FINISHED = 165  #: Notify that parameter estimation is finished and send the parameters to Alice.
    PE_APPROVED = (
        166  #: Accept the estimated parameters and proceed to the rest of the protocol.
    )
    PE_DENIED = 167  #: Deny the estimated parameters and abort.

    # Error Correction (180-199)
    EC_INITIALIZATION = 180
    EC_READY = 181
    EC_DENIED = 182
    EC_BLOCK = 183
    EC_BLOCK_ACK = 184
    EC_BLOCK_ERROR = 185
    EC_REMAINING = 186
    EC_REMAINING_ACK = 187
    EC_REMAINING_ERROR = 188
    EC_VERIFICATION = 189
    EC_VERIFICATION_SUCCESS = 190
    EC_VERIFICATION_FAIL = 191

    # Privacy Amplification (200-219)
    PA_REQUEST = 200
    PA_SUCCESS = 201
    PA_ERROR = 202

    # End of frame and End of communication (220-229)
    FRAME_ENDED = 220  #: End a frame.
    FRAME_ENDED_ACK = 221  #: ACK message for a end of frame.
    DISCONNECTION = 222  #: Notify the other party of a disconnection.
    DISCONNECTION_ACK = 223  #: ACK for the disconnection message.

    # Reserved (230-255)


class QOSSTErrorCodes(IntEnum):
    """Error codes for QOSST."""

    SOCKET_DISCONNECTION = -1  #: Indicate that the other party has disconnected
    FRAME_ERROR = -2  #: The frame was not well formatted
    AUTHENTICATION_FAILURE = (
        -3
    )  #: There was an authentication failure (either with the challenge wrong or not present, or on the signed digest)
    UNKOWN_CODE = -4  #: The sent code is not in the possible QOSST codes.
