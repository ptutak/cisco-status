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
    return RouterCredentials.model_validate_json(config)  # type: ignore
