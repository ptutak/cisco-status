import json
from pathlib import Path

import click

from .client import CiscoRouter, Router
from .credentials import RouterCredentials, parse_router_credentials
from .desired_config import DesiredHSRPConfig, parse_desired_hsrp_config
from .resolver import RouterHSRPResolver


@click.group()  # type: ignore
def cli() -> None:
    """Cisco Status Cli Tool."""


@cli.command()  # type: ignore
@click.option(  # type: ignore
    "-c",
    "--hsrp-config-file",
    type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False, path_type=Path),
    required=True,
    help="HSRP desired config file path.",
)
@click.option(  # type: ignore
    "-r",
    "--router-credentials",
    multiple=True,
    type=str,
    required=True,
    help="Provide router credentials in the format: Name,Host,Username,Password[,Secret]",
)
def hsrp_status(
    hsrp_config_file: Path,
    router_credentials: list[str],
) -> None:
    """Print the HSRP status of the routers."""  # noqa: DCO020
    with open(hsrp_config_file) as desired_config:
        desired_router_config = parse_desired_hsrp_config(desired_config.read())

    routers = [parse_router_credentials(router_creds) for router_creds in router_credentials]

    result = resolve_router_config(routers, desired_router_config, CiscoRouter)

    click.echo(json.dumps({"hsrp": result}, indent=2))


def resolve_router_config(
    routers_credentials: list[RouterCredentials],
    routers_config: list[DesiredHSRPConfig],
    router: type[Router],
) -> list[dict[str, list[dict[str, str]]]]:
    """Resolve the router config.

    Args:
        routers_credentials (list[RouterCredentials]): List of router credentials.
        routers_config (list[DesiredHSRPConfig]): List of desired router config.
        router (type[Router]): Router class.

    Raises:
        RuntimeError: If the router has no desired state.

    Returns:
        list[dict[str, list[dict[str, str]]]]: List of resolved router config.
    """
    desired_router_config = _contract_router_configs(routers_config)
    router_result: list[dict[str, list[dict[str, str]]]] = []

    # to make it more efficient we could use async parallelization here
    # but I didn't want to overcomplicate the code
    for credentials in routers_credentials:
        if credentials.name not in desired_router_config:
            raise RuntimeError(f"Router: {credentials.name} has no desired state.")
        concrete_router = router.from_credentials(credentials)
        resolver = RouterHSRPResolver(credentials.name, concrete_router, desired_router_config[credentials.name])
        router_result.append(resolver.resolve_router_config())

    return router_result


def _contract_router_configs(router_configs: list[DesiredHSRPConfig]) -> dict[str, list[DesiredHSRPConfig]]:
    result: dict[str, list[DesiredHSRPConfig]] = {}

    for config in router_configs:
        if config.name not in result:
            result[config.name] = []
        result[config.name].append(config)

    return result


if __name__ == "__main__":
    cli()  # pragma: no cover
