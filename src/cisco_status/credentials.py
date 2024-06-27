from pydantic import BaseModel


class RouterCredentials(BaseModel):  # type:ignore
    """Router credentials."""

    name: str
    host: str
    username: str
    password: str
    secret: str | None = None


def parse_router_credentials(config: str) -> RouterCredentials:
    """Parse the router credentials.

    Args:
        config (str): Router credentials config.

    Returns:
        RouterCredentials: Router credentials instance.
    """
    splitted_config = config.strip().split(",")
    return RouterCredentials(
        name=splitted_config[0],
        host=splitted_config[1],
        username=splitted_config[2],
        password=splitted_config[3],
        secret=splitted_config[4] if len(splitted_config) == 5 else None,
    )
