from typing import cast

from .client import Router
from .commands import CiscoConfigCommandParser, ShowStandbyBrief, StandbyConfig
from .desired_config import DesiredHSRPConfig
from .template_commands import TemplateCommand


class RouterHSRPResolver:
    _parser = CiscoConfigCommandParser.from_path(TemplateCommand.SHOW_STANDBY_BRIEF, ShowStandbyBrief)

    def __init__(self, name: str, router: Router, routers_desired_config: list[DesiredHSRPConfig]):
        self._name = name
        self._router = router
        self._desired_config = routers_desired_config

    def resolve_router_config(self) -> dict[str, dict[str, list[dict[str, str]]]]:
        result = self._router.show_standby_brief()
        command: ShowStandbyBrief = cast(ShowStandbyBrief, self._parser.parse(result))
        return self._get_router_standby_config(command.config, self._desired_config)

    def _get_router_standby_config(
        self, config: list[StandbyConfig], desired_config: list[DesiredHSRPConfig]
    ) -> dict[str, dict[str, list[dict[str, str]]]]:
        result: dict[str, dict[str, list[dict[str, str]]]] = {self._name: {}}
        for desired_config_entry in desired_config:
            passed = False
            for real_config in config:
                if (
                    desired_config_entry.interface == real_config.Interface
                    and desired_config_entry.group == real_config.Group
                    and desired_config_entry.state == real_config.State
                ):
                    passed = True
                    break

            if desired_config_entry.interface not in result[self._name]:
                result[self._name][desired_config_entry.interface] = []

            result[self._name][desired_config_entry.interface].append(
                {
                    "group": f"Group {desired_config_entry.group}",
                    "status": "Pass" if passed else f"Fail - No longer {desired_config_entry.state.value}",
                }
            )
        return result
