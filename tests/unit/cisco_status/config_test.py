from cisco_status.config import CiscoConfigParser

test_template = r"""Value Required X (\S+)
Value Required Y (\S+)

Start
    ^X\s+Y -> Record XY

XY
    ^${X}\s+${Y} -> Record XY
"""

def test_config_parser():
    parser = CiscoConfigParser(test_template)

    result = parser.parse("""
X   Y
3   4
5   6
""")
