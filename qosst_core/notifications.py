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
Module holding some utils function for notifications.
"""
import abc
import requests


# pylint: disable=too-few-public-methods
class QOSSTNotifier(abc.ABC):
    """
    An abstract notifier for QOSST.

    The only method that should be implemented is the
    send_notification method. Required variables should
    be passed throught the __init__ method.
    """

    @abc.abstractmethod
    def send_notification(self, message: str) -> None:
        """
        Send a notification whith the message passed as argument.

        Args:
            message (str): message to send as a notification.
        """


class FakeNotifier(QOSSTNotifier):
    """
    A Fake Notifier to be used as a default value.
    """

    def __init__(self, **_kwargs) -> None:
        """
        All args are ignored.
        """

    def send_notification(self, message: str) -> None:
        """
        Send notification for the dummy notifier. Does nothing.

        Args:
            message (str): message is ignored.
        """


class TelegramNotifier(QOSSTNotifier):
    """Notifier sending message to a particular chat using Telegram.


    Telegram servers are not opensource, and minimal information
    should be sent to telegram.

    This is actually a way to know when a function starts and when a function
    ends but should only be used this way and not sending critical information.
    """

    token: str  #: The token of the telegram bot.
    chat_id: int  #: The chat id where to send the message.

    BASE_TELEGRAM_API_URL: str = (
        "https://api.telegram.org/bot{token}/{method}"  #: API url of telegram.
    )

    def __init__(self, token: str, chat_id: int) -> None:
        """
        Args:
            token (str): token of the telegram bot.
            chat_id (int): the id of the chat where the message should be sent.
        """
        self.token = token
        self.chat_id = chat_id

    def send_notification(self, message: str) -> None:
        """Send the message to the configured chat_id using the telegram bot
        configured with the token.

        Args:
            message (str): message to send.
        """
        url = self.BASE_TELEGRAM_API_URL.format(token=self.token, method="sendMessage")
        requests.post(
            url,
            {"chat_id": self.chat_id, "text": message, "parse_mode": "MarkdownV2"},
            timeout=10,
        )
