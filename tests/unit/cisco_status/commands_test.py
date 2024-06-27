from cisco_status.commands import (
    CiscoConfigCommandParser,
    Command,
    ShowStandbyBrief,
    StandbyConfig,
)
from cisco_status.const import HSRPState

test_template = r"""Value Required X (\S+)
Value Required Y (\S+)

Start
  ^X\s+Y -> Record XY

XY
  ^${X}\s+${Y} -> Record XY
"""


class CommandXY(Command):
    def __init__(self, x: list[str], y: list[str]):
        self.x = x
        self.y = y

    @classmethod
    def parse(cls, config: str) -> "CommandXY":
        parser = CiscoConfigCommandParser.from_string(test_template)

        textfsm_config = parser.parse(config)

        xs: list[str] = []
        ys: list[str] = []

        for row in textfsm_config:
            xs.append(row[0])
            ys.append(row[1])

        return CommandXY(xs, ys)


def test_config_parser():
    result = CommandXY.parse(
        """
X   Y
3   4
5   6
"""
    )
    assert result.x == ["3", "5"]
    assert result.y == ["4", "6"]


def test_show_standby_brief():
    result = ShowStandbyBrief.parse(
        """
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    110 P Active  local           82.0.0.3        82.0.0.1
Gi0/0/1     2    105 P Standby 82.0.0.11       local           82.0.0.9
Gi0/0/1     2    105   Standby 82.0.0.11       local           82.0.0.9
"""
    )

    assert result.config == [
        StandbyConfig("Gi0/0/1", 1, 110, True, HSRPState.Active, "local", "82.0.0.3", "82.0.0.1"),
        StandbyConfig("Gi0/0/1", 2, 105, True, HSRPState.Standby, "82.0.0.11", "local", "82.0.0.9"),
        StandbyConfig("Gi0/0/1", 2, 105, False, HSRPState.Standby, "82.0.0.11", "local", "82.0.0.9"),
    ]
