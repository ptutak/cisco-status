import textfsm
import io

class CiscoConfigParser:
    def __init__(self, template: str | io.FileIO) -> None:
        self._parser = textfsm.TextFSM(template)

    def parse(self, config: str) -> list[str]:
        result = self._parser.ParseText(config)
        for row in result:
            print(row)
