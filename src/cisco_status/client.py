from abc import ABC, abstractmethod

from netmiko import BaseConnection, ConnectHandler


class Router(ABC):
    @abstractmethod
    def show_standby_brief(self) -> str:
        pass


class CiscoRouter(Router):
    DEFAULT_DEVICE = "cisco_ios"

    def __init__(
        self, host: str, username: str, password: str, secret: str | None = None, device_type: str = DEFAULT_DEVICE
    ) -> None:
        self._host = host
        self._username = username
        self._password = password
        self._secret = secret
        self._device_type = device_type

    def show_standby_brief(self) -> str:
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
            device_type=self._device_type,
            host=self._host,
            username=self._username,
            password=self._password,
            secret=self._secret,
        )
