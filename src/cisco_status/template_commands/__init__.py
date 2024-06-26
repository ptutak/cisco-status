from pathlib import Path

_PWD = Path(__file__)


class TemplateCommand:
    SHOW_STANDBY_BRIEF: Path = _PWD.parent / "show_standby_brief.textfsm"
