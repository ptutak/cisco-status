from cisco_status.credentials import parse_router_credentials

def test_parse_credentials():
    credentials = parse_router_credentials(r'{"name": "CE1", "host": "some-host", "username": "my_username", "password": "my_password"}')
    assert credentials.host == "some-host"
    assert credentials.name == "CE1"
    assert credentials.username == "my_username"
    assert credentials.password == "my_password"
