from pydantic import BaseModel


class RouterCredentials(BaseModel):  # type:ignore
    name: str
    host: str
    username: str
    password: str
    secret: str | None = None


def parse_router_credentials(config: str) -> RouterCredentials:
    return RouterCredentials.model_validate_json(config)  # type: ignore
