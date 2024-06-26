from pytest import fixture

from cisco_status.client import CiscoRouter
from cisco_status.credentials import RouterCredentials


@fixture
def my_cisco_mock(monkeypatch):
    class MyHandler:
        def __init__(self, args, kwargs):
            pass

        def find_prompt(self):
            return ""

        def send_command(self, command):
            return "xyzz"

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

    def get_my_connection(*args, **kwargs):
        return MyHandler(args, kwargs)

    monkeypatch.setattr(CiscoRouter, "_connection", get_my_connection)

    return MyHandler


def test_cisco_router(my_cisco_mock):

    router = CiscoRouter("some-host", "username", "password", "secret")

    assert router.show_standby_brief() == "xyzz"


def test_cisco_router_factory(my_cisco_mock):
    router = CiscoRouter.from_credentials(
        RouterCredentials(name="name", host="some-host", username="username", password="password", secret="secret")
    )

    assert isinstance(router, CiscoRouter)
    assert router.show_standby_brief() == "xyzz"
