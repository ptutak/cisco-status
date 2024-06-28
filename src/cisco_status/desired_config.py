import json
from typing import Any, cast

from pydantic import BaseModel, ConfigDict

from .const import HSRPState


class DesiredHSRPConfig(BaseModel):  # type:ignore
    """Desired HSRP configuration."""

    model_config = ConfigDict(extra="forbid")

    name: str
    group: int
    interface: str | None = None
    state: HSRPState

    @classmethod
    def from_dict(cls, name: str, router_desired_config: dict[str, Any]) -> "DesiredHSRPConfig":
        """Create a DesiredHSRPConfig instance from a dictionary.

        Args:
            name (str): Router name.
            router_desired_config (dict[str, Any]): Router desired config.

        Returns:
            DesiredHSRPConfig: Desired HSRP configuration instance.
        """
        return DesiredHSRPConfig(name=name, **router_desired_config)


def parse_desired_hsrp_config(config: str) -> list[DesiredHSRPConfig]:
    """Parse the desired HSRP configuration.

    Args:
        config (str): Desired HSRP configuration.

    Raises:
        RuntimeError: If the config is invalid.

    Returns:
        list[DesiredHSRPConfig]: List of desired HSRP configurations.
    """
    parsed_config: dict[str, Any] = json.loads(config)
    if "hsrp" not in parsed_config:
        raise RuntimeError("Invalid config - ho 'hsrp' section")

    router_configs: list[DesiredHSRPConfig] = []
    for router_config in parsed_config["hsrp"]:
        if len(router_config) != 1:
            raise RuntimeError("Invalid config - more than one router name for each router.")
        router_config = cast(dict[str, Any], router_config)
        router_name, desired_hsrp_configs = next(iter(router_config.items()))
        for desired_config in desired_hsrp_configs:
            router_configs.append(DesiredHSRPConfig.from_dict(router_name, desired_config))

    return router_configs
