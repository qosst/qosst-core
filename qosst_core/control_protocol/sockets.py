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
Network sockets for the QOSST control protocol.
"""
import abc
import socket
import json
from typing import Dict, Tuple, Type, Optional, Union
import secrets
import string
import hashlib
import logging
import selectors

from qosst_core.control_protocol import (
    DEFAULT_PORT,
    CHALLENGE_LENGTH,
    READING_BUFFER,
)
from qosst_core.control_protocol.codes import QOSSTCodes, QOSSTErrorCodes
from qosst_core.authentication.base import NoneAuthenticator, BaseAuthenticator

logger = logging.getLogger(__name__)


class QOSSTSocket(abc.ABC):
    """
    Base QOSST Socket (absract).

    Implements the recv and send function.
    """

    host: str  #: Host (to connect or to bind)
    port: int  #: Port (to connect or to bind)
    socket: Optional[socket.socket]  #: Socket (making the communication)
    auth: BaseAuthenticator  #: Signing and verifying digests
    selector: selectors.BaseSelector  #: Selector for read

    challenge: str  #: Previous or next challenge

    def __init__(
        self,
        host="127.0.0.1",
        port: int = DEFAULT_PORT,
        authenticator: Type[BaseAuthenticator] = NoneAuthenticator,
        authentication_params: Optional[Dict] = None,
    ):
        """
        Args:
            host (str, optional): either the port to connect to or to bind to. Defaults to "127.0.0.1".
            port (int, optional): either the port to connect to or to bind to. Defaults to DEFAULT_PORT.
            authenticator (Type[BaseAuthenticator], optional): Authenticator to generate and check digests. Defaults to NoneAuthenticator.
            authentication_params (Optional[dict], optional): Parameters to be given to the authentication class. Defaults to {}.
        """
        self.host = host
        self.port = port
        self.socket = None
        if authentication_params is None:
            authentication_params = {}
        self.auth = authenticator(**authentication_params)
        self.challenge = ""
        self.selector = selectors.DefaultSelector()

    @abc.abstractmethod
    def open(self):
        """
        Open socket.
        """

    def connect(self):
        """
        Connect socket (connect to server or wait for clients).
        """
        logger.debug("Setting selector and socket to non-blocking.")
        self.socket.setblocking(False)
        self.selector.register(
            self.socket,
            selectors.EVENT_READ,
        )

    def send(self, code: QOSSTCodes, data: Optional[Dict] = None):
        """
        Send a message with code and data.

        Args:
            code (QOSSTCodes): the code of the message to send.
            data (Dict, optional): content of the message. Defaults to None.
        """
        if not self.socket:
            raise OSError("Socket is not connected. Impossible to send data.")
        # Set the socket to blocking
        self.socket.setblocking(True)
        # Transform data to bytes
        if data:
            data_bytes = json.dumps(data).encode("utf-8")
        else:
            data_bytes = b""

        # Generate the variable length header
        # Put the challenge requested by the other party
        # Generate the next challenge for the other party
        next_challenge = "".join(
            [
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(CHALLENGE_LENGTH)
            ]
        )
        variable_header = {
            "code": code,
            "content_length": len(data_bytes),
            "challenge": self.challenge,
            "next_challenge": next_challenge,
        }

        variable_header_bytes = json.dumps(variable_header).encode("utf-8")

        # Save the challenge for the other party in memory
        self.challenge = next_challenge

        # Compute the message and its digest
        message = variable_header_bytes + data_bytes
        digest = hashlib.sha256(message).digest()

        # Sign the digest using the signing function
        signed_digest = self.auth.sign_digest(digest)

        # Compute the fixed header
        fixed_header = len(variable_header_bytes).to_bytes(2, "big") + len(
            signed_digest
        ).to_bytes(2, "big")

        # Send everything to the wire
        logger.info(
            "Sending frame with code %s (%i) and %i bytes of data",
            str(code),
            int(code),
            len(data_bytes),
        )
        logger.debug("Data: %s", str(data))
        self.socket.sendall(fixed_header + signed_digest + message)

        # Now set the socket to non-blocking again
        self.socket.setblocking(False)

    # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches,too-many-statements
    def recv(self) -> Tuple[Union[QOSSTCodes, QOSSTErrorCodes], Optional[Dict]]:
        """
        Receive a message from the network and return code and data.

        Returns:
            Tuple[Union[QOSSTCodes, QOSSTErrorCodes], Optional[Dict]]: the code of the message (or the error code) and the optional content of the message.
        """
        if not self.socket:
            raise OSError("Socket is not connected. Impossible to receive data.")
        readable = False
        while not readable:
            events = self.selector.select(timeout=0.1)
            for _, mask in events:
                if mask * selectors.EVENT_READ:
                    readable = True

        self.socket.setblocking(True)
        recv_buffer = b""
        while len(recv_buffer) < 4:
            try:
                received_data = self.socket.recv(READING_BUFFER)
            except ConnectionError:
                received_data = b""
            if not received_data:
                # The other party has disconnected
                logger.warning("Socket disconnected.")
                return QOSSTErrorCodes.SOCKET_DISCONNECTION, None

            recv_buffer += received_data

            # First the two first bytes to get size of the header
            header_size = int.from_bytes(recv_buffer[:2], "big")
            recv_buffer = recv_buffer[2:]

            # Then read the size the size of the digest
            digest_size = int.from_bytes(recv_buffer[:2], "big")
            recv_buffer = recv_buffer[2:]

        # Now wait until we can read the digest
        while len(recv_buffer) < digest_size:
            try:
                received_data = self.socket.recv(READING_BUFFER)
            except ConnectionError:
                received_data = b""
            if not received_data:
                logger.error(
                    "Frame too short (waiting for digest and %i < %i)",
                    len(recv_buffer),
                    digest_size,
                )
                self.socket.setblocking(False)
                return QOSSTErrorCodes.FRAME_ERROR, None
            recv_buffer += received_data

        # Read the digest
        signed_digest = recv_buffer[:digest_size]
        recv_buffer = recv_buffer[digest_size:]

        # Now wait until we can read the header
        while len(recv_buffer) < header_size:
            try:
                received_data = self.socket.recv(READING_BUFFER)
            except ConnectionError:
                received_data = b""
            if not received_data:
                logger.error(
                    "Frame too short (waiting for header and %i < %i)",
                    len(recv_buffer),
                    header_size,
                )
                self.socket.setblocking(False)
                return QOSSTErrorCodes.FRAME_ERROR, None
            recv_buffer += received_data

        header_bytes = recv_buffer[:header_size]

        # Try to decode the header
        try:
            header = json.loads(header_bytes.decode("utf-8"))
        except json.JSONDecodeError as exc:
            logger.error("Error while decoding the JSON header (%s).", str(exc))
            self.socket.setblocking(False)
            return QOSSTErrorCodes.FRAME_ERROR, None

        recv_buffer = recv_buffer[header_size:]

        # Now verify that the header is well formed.
        if (
            not "code" in header
            or not "challenge" in header
            or not "next_challenge" in header
            or not "content_length" in header
        ):
            logger.error("Malformed header (%s).", str(header))
            self.socket.setblocking(False)
            return QOSSTErrorCodes.FRAME_ERROR, None

        content_length = header["content_length"]

        # Now read the content
        if content_length:
            # Now wait until we can read the content
            while len(recv_buffer) < content_length:
                try:
                    received_data = self.socket.recv(READING_BUFFER)
                except ConnectionError:
                    received_data = b""
                if not received_data:
                    logger.error(
                        "Frame too short (waiting for content and %i < %i)",
                        len(recv_buffer),
                        content_length,
                    )
                    self.socket.setblocking(False)
                    return QOSSTErrorCodes.FRAME_ERROR, None
                recv_buffer += received_data

            content_bytes = recv_buffer[:content_length]
            # Try to decode the content
            try:
                content = json.loads(content_bytes.decode("utf-8"))
            except json.JSONDecodeError as exc:
                logger.error("Error while decoding the JSON content (%s).", str(exc))
                self.socket.setblocking(False)
                return QOSSTErrorCodes.FRAME_ERROR, None
        else:
            content_bytes = b""
            content = None

        # Test if code is a QOSST code
        try:
            code = QOSSTCodes(header["code"])
        except ValueError as exc:
            logger.error("%s is not a valid code (%s)", str(header["code"]), str(exc))
            self.socket.setblocking(False)
            return QOSSTErrorCodes.UNKOWN_CODE, None

        # Compute hash
        digest = hashlib.sha256(header_bytes + content_bytes).digest()

        # Verify signature of the digest
        if not self.auth.check_digest(digest, signed_digest):
            logger.error("Signature on digest is wrong.")
            self.socket.setblocking(False)
            return QOSSTErrorCodes.AUTHENTICATION_FAILURE, None

        # Verify that the challenge is valid
        if (
            not self.challenge == header["challenge"]
            and code != QOSSTCodes.IDENTIFICATION_REQUEST
        ):
            # We shouldn't fail on IDENTIFICATION_REQUEST since it's the one
            # that initialize or reinitialize the authenthication.
            logger.error(
                "The requested challenge is wrong (%s != %s).",
                self.challenge,
                header["challenge"],
            )
            self.socket.setblocking(False)
            return QOSSTErrorCodes.AUTHENTICATION_FAILURE, None

        # save next challenge for sending
        self.challenge = header["next_challenge"]

        # Finally return to higher layers
        logger.info(
            "Frame received with code %s (%i) and %i bytes of data",
            str(code),
            int(code),
            content_length,
        )
        logger.debug("Data: %s", str(content))
        self.socket.setblocking(False)
        return code, content

    def close(self):
        """
        Close socket.
        """
        if self.socket:
            try:
                self.selector.unregister(self.socket)
            except KeyError:  #  The socket is not registered yet
                pass
            self.socket.close()


class QOSSTClient(QOSSTSocket):
    """
    Specific class for the QOSST client.
    """

    def open(self) -> None:
        """
        Open socket.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """
        Connect to server.
        """
        if not self.socket:
            raise OSError("Socket has not yet been opened. Impossible to connect.")
        self.socket.connect((self.host, self.port))
        logger.info(
            "Successfully connected to host %s on port %i", self.host, self.port
        )
        super().connect()

    def request(
        self, code: QOSSTCodes, data: Optional[Dict] = None
    ) -> Tuple[Union[QOSSTCodes, QOSSTErrorCodes], Optional[Dict]]:
        """Send a message to the server and wait for a response.

        In case of a disconnection, the client will try to reconnect.

        Args:
            code (QOSSTCodes): the code of the message to send.
            data (Dict, optional): the content of the message to send. Defaults to None.

        Returns:
            Tuple[Union[QOSSTCodes, QOSSTErrorCodes], Optional[Dict]]:: the code and the content of the received message.
        """
        # Send the message
        self.send(code, data)

        # Now wait for a response
        received_code, received_data = self.recv()

        # If the code is a disconnection, try to connect and send again.
        if received_code == QOSSTErrorCodes.SOCKET_DISCONNECTION:
            logger.error("Received a disonnection during request. Connecting again.")
            self.connect()
            return self.request(code, data)
        return received_code, received_data


class QOSSTServer(QOSSTSocket):
    """
    Specific class for the QOSST Server.
    """

    host_socket: socket.socket  #: Host socket.
    client_address: str  #: Address of the client.

    def open(self) -> None:
        """
        Open host socket.
        """
        logger.info("Binding to socket on address %s port %i", self.host, self.port)
        self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_socket.bind((self.host, self.port))

    def connect(self) -> None:
        """
        Wait for a client to connect.
        """
        logger.info("Waiting for a client to connect")
        self.host_socket.listen(1)
        self.host_socket.setblocking(False)
        self.selector.register(self.host_socket, selectors.EVENT_READ)
        acceptable = False
        while not acceptable:
            events = self.selector.select(timeout=0.1)
            for key, mask in events:
                if (
                    key.data is None
                    and mask & selectors.EVENT_READ
                    and key.fileobj == self.host_socket
                ):
                    acceptable = True
        (self.socket, self.client_address) = self.host_socket.accept()
        self.host_socket.setblocking(True)
        self.selector.unregister(self.host_socket)
        logger.info("Client with address %s has connected", self.client_address)
        super().connect()

    def recv(self) -> Tuple[Union[QOSSTCodes, QOSSTErrorCodes], Optional[Dict]]:
        """Receive a message.

        In case of a disconnection, the client socket is closed.

        Returns:
            Tuple[Union[QOSSTCodes, QOSSTErrorCodes], Optional[Dict]]: the code of the received message (or the error code) and the optional message.
        """
        code, data = super().recv()
        if code == QOSSTErrorCodes.SOCKET_DISCONNECTION and self.socket:
            self.selector.unregister(self.socket)
            self.socket.close()
            self.socket = None
        return code, data

    def close(self) -> None:
        """
        Close the socket. Also close the host socket.
        """
        if self.host_socket:
            self.host_socket.close()
        super().close()
