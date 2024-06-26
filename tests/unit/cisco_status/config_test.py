from cisco_status.config import CiscoConfigCommandParser, Command, ShowStandbyBrief

test_template = r"""Value Required X (\S+)
Value Required Y (\S+)

Start
  ^X\s+Y -> Record XY

XY
  ^${X}\s+${Y} -> Record XY
"""


class CommandXY(Command):
    def __init__(self, x: list[str], y: list[str]):
        self._x = x
        self._y = y

    @classmethod
    def parse(cls, textfsm_config: list[list[str]]) -> "CommandXY":
        xs: list[str] = []
        ys: list[str] = []

        for row in textfsm_config:
            xs.append(row[0])
            ys.append(row[1])

        return CommandXY(xs, ys)

    def print(self) -> None:
        print(self._x)
        print(self._y)


def test_config_parser():
    parser = CiscoConfigCommandParser.from_string(test_template, CommandXY)

    result = parser.parse("""
X   Y
3   4
5   6
""")

    result.print()


def test_show_standby_brief():
    parser = CiscoConfigCommandParser
