import os
from typing import Any
from .const import HSRPState
from pydantic import BaseModel


class DesiredHSRPConfig(BaseModel):
    name: str
    host: str
    username: str
    password: str
    interface: str
    group: int
    state: HSRPState

    @classmethod
    def from_dict(cls, router_desired_config: dict[str, Any]) -> "DesiredHSRPConfig":
        return cls(**router_desired_config)
