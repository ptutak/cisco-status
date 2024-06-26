from cisco_status.const import HSRPState
from cisco_status.desired_config import DesiredHSRPConfig, parse_desired_hsrp_config


def test_desired_config_parse():
    config = {
        "name": "CE1",
        "interface": "Gi0/0/1",
        "group": 1,
        "state": "Active",
    }

    result = DesiredHSRPConfig.from_dict(config)

    assert result.name == "CE1"
    assert result.interface == "Gi0/0/1"
    assert result.group == 1
    assert result.state == HSRPState.Active


def test_parse_desired_config():
    desired_config = """{
    "hsrp": [
        {
            "name": "CE1",
            "interface": "Gi0/0/1",
            "group": 1,
            "state": "Active"
        },
        {
            "name": "CE1",
            "interface": "Gi0/0/1",
            "group": 2,
            "state": "Standby"
        }
    ]
}
"""
    result = parse_desired_hsrp_config(desired_config)

    expected_result = [
        DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=1, state=HSRPState.Active),
        DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=2, state=HSRPState.Standby),
    ]

    assert result == expected_result
