from pathlib import Path
from typing import cast

import click

from .client import CiscoRouter
from .commands import CiscoConfigCommandParser, ShowStandbyBrief
from .credentials import RouterCredentials, parse_router_credentials
from .desired_config import DesiredHSRPConfig, parse_desired_hsrp_config
from .template_commands import TemplateCommand


@click.group()
def cli() -> None:
    """Cli Group."""


@cli.command()  # type: ignore
@click.option(  # type: ignore
    "--hsrp-config-file", type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False, path_type=Path)
)
@click.option("-r", "--router-credentials", multiple=True, type=str)  # type: ignore
def hsrp_status(
    hsrp_config_file: Path,
    router_credentials: list[str],
) -> None:
    with open(hsrp_config_file) as desired_config:
        desired_router_config = parse_desired_hsrp_config(desired_config.read())

    routers = [parse_router_credentials(router_creds) for router_creds in router_credentials]


def _resolve_router_config(routers_credentials: list[RouterCredentials], routers_config: list[DesiredHSRPConfig]):
    router_result: dict[str, list[dict[str, str]]] = {}
    parser = CiscoConfigCommandParser.from_path(TemplateCommand.SHOW_STANDBY_BRIEF, ShowStandbyBrief)
    for credentials in routers_credentials:
        router = CiscoRouter.from_credentials(credentials)
        show_standby_brief_command_result = router.show_standby_brief()
        command: ShowStandbyBrief = cast(ShowStandbyBrief, parser.parse(show_standby_brief_command_result))
