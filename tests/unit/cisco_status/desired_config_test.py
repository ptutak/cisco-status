from cisco_status.desired_config import DesiredHSRPConfig
from cisco_status.const import HSRPState


def test_desired_config_parse():
    config = {
        "name": "CE1",
        "host": "192.168.0.1",
        "username": "USER",
        "password": "PASS",
        "interface": "Gi0/0/1",
        "group": 1,
        "state": "Active",
    }

    result = DesiredHSRPConfig.from_dict(config)

    assert result.name == "CE1"
    assert result.host == "192.168.0.1"
    assert result.username == "USER"
    assert result.password == "PASS"
    assert result.interface == "Gi0/0/1"
    assert result.group == 1
    assert result.state == HSRPState.Active
