import io
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import textfsm

from .const import HSRPState
from .template_commands import TemplateCommand


class Command(ABC):
    """Command interface."""

    @classmethod
    @abstractmethod
    def parse(cls, config: str) -> "Command":
        """Parse the command into a concrete struct.

        Args:
            config (str): Command output.
        """


class CiscoConfigCommandParser:
    """Cisco configuration command parser."""

    def __init__(self, template: io.IOBase) -> None:
        """Create a new CiscoConfigCommandParser instance.

        Args:
            template (io.IOBase): Template file.
        """
        self._config_parser = textfsm.TextFSM(template)

    def parse(self, config: str) -> list[list[str]]:
        """Parse the configuration.

        Args:
            config (str): Configuration to parse.

        Returns:
            list[list[str]]: Parsed configuration.
        """
        result = self._config_parser.ParseText(config)
        self._config_parser.Reset()
        return result  # type: ignore

    @classmethod
    def from_string(cls, template: str) -> "CiscoConfigCommandParser":
        """Create a new CiscoConfigCommandParser instance from a string.

        Args:
            template (str): Template string.

        Returns:
            CiscoConfigCommandParser: Instance of the parser.
        """
        return cls(io.StringIO(template))

    @classmethod
    def from_path(cls, template_path: os.PathLike[str]) -> "CiscoConfigCommandParser":
        """Create a new CiscoConfigCommandParser instance from a path.

        Args:
            template_path (os.PathLike[str]): Path to the template file.

        Returns:
            CiscoConfigCommandParser: Instance of the parser.
        """
        with open(template_path) as file:
            return cls(file)


@dataclass(frozen=True)
class StandbyConfig:
    """Standby configuration."""

    interface: str
    group: int
    priority: int
    preemptive: bool
    state: HSRPState
    active: str
    standby: str
    virtualIP: str


class ShowStandbyBrief(Command):
    """Show standby brief command."""

    def __init__(self, config: list[StandbyConfig]):
        """Create a new ShowStandbyBrief instance.

        Args:
            config (list[StandbyConfig]): Standby configuration.
        """
        self.config = config

    @classmethod
    def parse(cls, config: str) -> "ShowStandbyBrief":
        """Parse the show standby brief command.

        Args:
            config (str): Command output.

        Returns:
            ShowStandbyBrief: Instance of the command.
        """
        parser = CiscoConfigCommandParser.from_path(TemplateCommand.SHOW_STANDBY_BRIEF)
        textfsm_output = parser.parse(config)
        configs: list[StandbyConfig] = []

        for row in textfsm_output:
            configs.append(
                StandbyConfig(
                    row[0],
                    int(row[1]),
                    int(row[2]),
                    True if row[3] == "P" else False,
                    HSRPState(row[4]),
                    row[5],
                    row[6],
                    row[7],
                )
            )

        return cls(configs)
