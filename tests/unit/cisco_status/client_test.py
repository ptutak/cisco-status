import netmiko

class MyHandler:
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
        self.commands = []

    def find_prompt(self):
        return ""

    def send_command(self, command):
        self.commands.append(command)
        return "xyzz"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

def get_my_connect_handler(*args, **kwargs):
    return MyHandler(args, kwargs)

def test_cisco_router(monkeypatch):
    monkeypatch.setattr(netmiko, "ConnectHandler", get_my_connect_handler)
    from cisco_status.client import CiscoRouter

    router = CiscoRouter("some-host", "username", "password", "secret")

    assert router.show_standby_brief() == "xyzz"
