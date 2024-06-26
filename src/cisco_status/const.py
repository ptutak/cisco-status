from enum import Enum


class HSRPState(Enum):
    Active: str = "Active"
    Standby: str = "Standby"
    Speak: str = "Speak"
    Listen: str = "Listen"
    Init: str = "Init"
    Disabled: str = "Disabled"
