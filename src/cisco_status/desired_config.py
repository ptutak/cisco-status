import json
from typing import Any

from pydantic import BaseModel

from .const import HSRPState

class DesiredHSRPConfig(BaseModel):
    name: str
    interface: str
    group: int
    state: HSRPState

    @classmethod
    def from_dict(cls, router_desired_config: dict[str, Any]) -> "DesiredHSRPConfig":
        return cls(**router_desired_config)



def parse_desired_hsrp_config(config: str) -> list[DesiredHSRPConfig]:
    parsed_config: dict[str, Any] = json.loads(config)
    if "hsrp" not in parsed_config:
        raise RuntimeError("Invalid config")

    router_configs: list[DesiredHSRPConfig] = []
    for router_config in parsed_config["hsrp"]:
        router_configs.append(DesiredHSRPConfig.from_dict(router_config))

    return router_configs
