from abc import ABC, abstractmethod

from netmiko import BaseConnection, ConnectHandler

from .credentials import RouterCredentials


class Router(ABC):
    """Router interface."""

    @abstractmethod
    def show_standby_brief(self) -> str:
        """Return the show standby brief command result."""

    @classmethod
    @abstractmethod
    def from_credentials(cls, credentials: RouterCredentials) -> "Router":
        """Create a router instance from credentials.

        Args:
            credentials (RouterCredentials): Router credentials.
        """


class CiscoRouter(Router):
    """Cisco router implementation."""

    DEFAULT_DEVICE = "cisco_ios"

    def __init__(self, host: str, username: str, password: str, secret: str | None = None) -> None:
        """Create a new CiscoRouter instance.

        Args:
            host (str): Hostname or IP address of the device.
            username (str): Username to authenticate with the device.
            password (str): Password to authenticate with the device.
            secret (str | None, optional): Optional secret. Defaults to None.
        """
        self._host = host
        self._username = username
        self._password = password
        self._secret = secret

    def show_standby_brief(self) -> str:
        """Return the show standby brief command result.

        Raises:
            RuntimeError: If the output is not a string or a list.

        Returns:
            str: Output of the command.
        """
        with self._connection() as connection:
            connection.find_prompt()
            result = connection.send_command("show standby brief")
            if isinstance(result, str):
                return result
            if isinstance(result, list):
                return "\n".join(str(line) for line in result)
            raise RuntimeError("Wrong output")

    def _connection(self) -> BaseConnection:
        return ConnectHandler(
            device_type=self.DEFAULT_DEVICE,
            host=self._host,
            username=self._username,
            password=self._password,
            secret=self._secret,
        )

    @classmethod
    def from_credentials(cls, credentials: RouterCredentials) -> "CiscoRouter":
        """Create a router instance from credentials.

        Args:
            credentials (RouterCredentials): Router credentials.

        Returns:
            CiscoRouter: Created router instance.
        """
        return cls(credentials.host, credentials.username, credentials.password, credentials.secret)
