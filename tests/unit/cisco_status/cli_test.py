from pytest import fixture

from cisco_status.cli import CiscoRouter, resolve_router_config


class MyRouter:
    def __init__(self, args, kwargs):
        self.args = args

    def find_prompt(self):
        return ""

    def send_command(self, command):
        return

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None


@fixture
def my_cisco_mock(monkeypatch):

    def get_my_router(*args, **kwargs):
        return MyRouter(args, kwargs)

    monkeypatch.setattr(CiscoRouter, "from_credentials", get_my_router)

    return MyRouter


def test_resolve_router_config():
    credentials = None
    resolve_router_config()

    assert True
