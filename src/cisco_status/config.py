from abc import ABC, abstractmethod
import textfsm
import io
import os


class CommandParser(ABC):
    @classmethod
    def from_config(cls, textfsm_output: list[list[str]]) -> "CommandParser":
        return cls(textfsm_output)

    @abstractmethod
    def parse(self, textfsm_output: list[list[str]]):
        """_summary_

        Args:
            textfsm_output (list[list[str]]): _description_

        Returns:
            _type_: _description_
        """


class CiscoConfigParser:
    def __init__(self, template: io.FileIO, ) -> None:
        self._parser = textfsm.TextFSM(template)

    def parse(self, config: str) -> list[str]:
        result = self._parser.ParseText(config)

    @classmethod
    def from_string(cls, template: str) -> "CiscoConfigParser":
        return cls(io.StringIO(template))

    @classmethod
    def from_path(cls, template_path: os.PathLike):
        with open(template_path) as file:
            return cls(file)


class HSRPConfig
