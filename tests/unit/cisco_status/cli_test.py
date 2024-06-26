from pytest import fixture

from cisco_status.cli import DesiredHSRPConfig, RouterCredentials, resolve_router_config
from cisco_status.const import HSRPState


class MyRouter:
    def __init__(self, creds: RouterCredentials):
        self._creds = creds

    def show_standby_brief(self):
        if self._creds.name == "CE1":
            return """Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    110 P Active  local           82.0.0.3        82.0.0.1
Gi0/0/1     2    105 P Standby 82.0.0.11       local           82.0.0.9
"""
        if self._creds.name == "CE2":
            return """Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    105 P Standby 82.0.0.2        local           82.0.0.1
Gi0/0/1     2    110 P Active  local           82.0.0.10       82.0.0.9
"""
        return ""

    @classmethod
    def from_credentials(cls, creds: RouterCredentials):
        return MyRouter(creds)


def test_resolve_router_config():
    credentials = [
        RouterCredentials(name="CE1", host="host-1", username="username-1", password="password-1"),
        RouterCredentials(name="CE2", host="host-2", username="username-2", password="password-2"),
    ]

    desired_configs = [
        DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=1, state=HSRPState.Active),
        DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=2, state=HSRPState.Standby),
        DesiredHSRPConfig(name="CE2", interface="Gi0/0/1", group=1, state=HSRPState.Standby),
        DesiredHSRPConfig(name="CE2", interface="Gi0/0/1", group=2, state=HSRPState.Active),
    ]
    result = resolve_router_config(credentials, desired_configs, MyRouter)

    assert result == [
        {"CE1": {"Gi0/0/1": [{"group": "Group 1", "status": "Pass"}, {"group": "Group 2", "status": "Pass"}]}},
        {"CE2": {"Gi0/0/1": [{"group": "Group 1", "status": "Pass"}, {"group": "Group 2", "status": "Pass"}]}},
    ]


def test_resolve_router_config_fail():
    credentials = [
        RouterCredentials(name="CE1", host="host-1", username="username-1", password="password-1"),
        RouterCredentials(name="CE2", host="host-2", username="username-2", password="password-2"),
    ]

    desired_configs = [
        DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=1, state=HSRPState.Standby),
        DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=2, state=HSRPState.Standby),
        DesiredHSRPConfig(name="CE2", interface="Gi0/0/1", group=1, state=HSRPState.Standby),
        DesiredHSRPConfig(name="CE2", interface="Gi0/0/1", group=2, state=HSRPState.Standby),
    ]
    result = resolve_router_config(credentials, desired_configs, MyRouter)

    assert result == [
        {
            "CE1": {
                "Gi0/0/1": [
                    {"group": "Group 1", "status": "Fail - No longer Standby"},
                    {"group": "Group 2", "status": "Pass"},
                ]
            }
        },
        {
            "CE2": {
                "Gi0/0/1": [
                    {"group": "Group 1", "status": "Pass"},
                    {"group": "Group 2", "status": "Fail - No longer Standby"},
                ]
            }
        },
    ]


# TODO: cli tests
