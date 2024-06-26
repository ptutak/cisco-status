from cisco_status.const import HSRPState
from cisco_status.credentials import RouterCredentials
from cisco_status.resolver import DesiredHSRPConfig, Router, RouterHSRPResolver


class MyRouter(Router):
    def show_standby_brief(self):
        return """Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    110 P Active  local           82.0.0.3        82.0.0.1
Gi0/0/1     2    105 P Standby 82.0.0.11       local           82.0.0.9"""

    @classmethod
    def from_credentials(cls, credentials: RouterCredentials) -> Router:
        return super().from_credentials(credentials)


def test_resolver():
    resolver = RouterHSRPResolver(
        "CE1",
        MyRouter(),
        [
            DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=1, state=HSRPState.Active),
            DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=2, state=HSRPState.Standby),
        ],
    )

    assert resolver.resolve_router_config() == {
        "CE1": {"Gi0/0/1": [{"group": "Group 1", "status": "Pass"}, {"group": "Group 2", "status": "Pass"}]}
    }


def test_resolver_fail():
    resolver = RouterHSRPResolver(
        "CE1",
        MyRouter(),
        [
            DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=1, state=HSRPState.Standby),
            DesiredHSRPConfig(name="CE1", interface="Gi0/0/1", group=2, state=HSRPState.Standby),
        ],
    )

    assert resolver.resolve_router_config() == {
        "CE1": {
            "Gi0/0/1": [
                {"group": "Group 1", "status": "Fail - No longer Standby"},
                {"group": "Group 2", "status": "Pass"},
            ]
        }
    }
