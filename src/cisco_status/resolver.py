from .client import Router
from .commands import ShowStandbyBrief, StandbyConfig
from .desired_config import DesiredHSRPConfig


class RouterHSRPResolver:
    """Router HSRP Resolver."""

    def __init__(self, name: str, router: Router, routers_desired_config: list[DesiredHSRPConfig]):
        """Create a new RouterHSRPResolver instance.

        Args:
            name (str): Router name.
            router (Router): Router client.
            routers_desired_config (list[DesiredHSRPConfig]): List of desired router config.
        """
        self._name = name
        self._router = router
        self._desired_config = routers_desired_config

    def resolve_router_config(self) -> dict[str, list[dict[str, str]]]:
        """Resolve the router config.

        Returns:
            dict[str, dict[str, list[dict[str, str]]]]: Resolved router config.
        """
        result = self._router.show_standby_brief()
        command: ShowStandbyBrief = ShowStandbyBrief.parse(result)
        return self._get_router_standby_config(command.config, self._desired_config)

    def _get_router_standby_config(
        self, config: list[StandbyConfig], desired_config: list[DesiredHSRPConfig]
    ) -> dict[str, list[dict[str, str]]]:
        result: dict[str, list[dict[str, str]]] = {self._name: []}

        # we could use a more efficient algorithm here in case of large number of desired configs
        for desired_config_entry in desired_config:
            passed = False
            for real_config in config:
                if self._check_config(real_config, desired_config_entry):
                    passed = True
                    break

            result[self._name].append(
                {
                    "group": f"Group {desired_config_entry.group}",
                    "status": "Pass" if passed else f"Fail - No longer {desired_config_entry.state.value}",
                }
            )
        return result

    def _check_config(self, standby_config: StandbyConfig, desired_config: DesiredHSRPConfig) -> bool:
        if desired_config.interface is not None:
            return (
                desired_config.group == standby_config.group
                and desired_config.state == standby_config.state
                and desired_config.interface == standby_config.interface
            )
        return desired_config.group == standby_config.group and desired_config.state == standby_config.state
