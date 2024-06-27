import json
from typing import Any

from pydantic import BaseModel, ConfigDict

from .const import HSRPState


class DesiredHSRPConfig(BaseModel):  # type:ignore
    """Desired HSRP configuration."""
    model_config = ConfigDict(extra="forbid")

    name: str
    group: int
    state: HSRPState

    @classmethod
    def from_dict(cls, router_desired_config: dict[str, Any]) -> "DesiredHSRPConfig":
        """Create a DesiredHSRPConfig instance from a dictionary.

        Args:
            router_desired_config (dict[str, Any]): Router desired config.

        Returns:
            DesiredHSRPConfig: Desired HSRP configuration instance.
        """
        return DesiredHSRPConfig.model_validate(router_desired_config)


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
        raise RuntimeError("Invalid config")

    router_configs: list[DesiredHSRPConfig] = []
    for router_config in parsed_config["hsrp"]:
        router_configs.append(DesiredHSRPConfig.from_dict(router_config))

    return router_configs
