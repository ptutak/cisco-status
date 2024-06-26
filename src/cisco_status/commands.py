import io
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import textfsm

from .const import HSRPState


class Command(ABC):
    @abstractmethod
    def print(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def parse(cls, textfsm_output: list[list[str]]) -> "Command":
        """Parse the command into a concrete struct.

        Args:
            textfsm_output (list[list[str]]): Textfsm output parsed from a router.

        Returns:
            Command: A created command.
        """


class CiscoConfigCommandParser:
    def __init__(self, template: io.IOBase, command_parser: type[Command]) -> None:
        self._config_parser = textfsm.TextFSM(template)
        self._command_parser = command_parser

    def parse(self, config: str) -> Command:
        result = self._config_parser.ParseText(config)
        self._config_parser.Reset()
        return self._command_parser.parse(result)

    @classmethod
    def from_string(cls, template: str, command_parser: type[Command]) -> "CiscoConfigCommandParser":
        return cls(io.StringIO(template), command_parser)

    @classmethod
    def from_path(cls, template_path: os.PathLike[str], command_parser: type[Command]) -> "CiscoConfigCommandParser":
        with open(template_path) as file:
            return cls(file, command_parser)


@dataclass(frozen=True)
class StandbyConfig:
    Interface: str
    Group: int
    Priority: int
    Preemptive: str
    State: HSRPState
    Active: str
    Standby: str
    VirtualIP: str


class ShowStandbyBrief(Command):
    def __init__(self, config: list[StandbyConfig]):
        self.config = config

    @classmethod
    def parse(cls, textfsm_output: list[list[str]]) -> "ShowStandbyBrief":
        configs: list[StandbyConfig] = []

        for row in textfsm_output:
            configs.append(
                StandbyConfig(row[0], int(row[1]), int(row[2]), row[3], HSRPState(row[4]), row[5], row[6], row[7])
            )

        return cls(configs)

    def print(self) -> None:
        for config in self.config:
            print(config)
