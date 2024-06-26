import json
from pathlib import Path

import click

from .client import CiscoRouter
from .credentials import RouterCredentials, parse_router_credentials
from .desired_config import DesiredHSRPConfig, parse_desired_hsrp_config
from .resolver import RouterHSRPResolver


@click.group()  # type: ignore
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

    result = resolve_router_config(routers, desired_router_config)

    click.echo(json.dumps(result, indent=2))


def resolve_router_config(
    routers_credentials: list[RouterCredentials], routers_config: list[DesiredHSRPConfig]
) -> list[dict[str, dict[str, list[dict[str, str]]]]]:
    desired_router_config = _contract_router_configs(routers_config)
    router_result: list[dict[str, dict[str, list[dict[str, str]]]]] = []

    for credentials in routers_credentials:
        if credentials.name not in desired_router_config:
            raise RuntimeError(f"Router: {credentials.name} has no desired state.")
        router = CiscoRouter.from_credentials(credentials)
        resolver = RouterHSRPResolver(credentials.name, router, desired_router_config[credentials.name])
        router_result.append(resolver.resolve_router_config())

    return router_result


def _contract_router_configs(router_configs: list[DesiredHSRPConfig]) -> dict[str, list[DesiredHSRPConfig]]:
    result: dict[str, list[DesiredHSRPConfig]] = {}

    for config in router_configs:
        if config.name not in result:
            result[config.name] = []
        result[config.name].append(config)

    return result
