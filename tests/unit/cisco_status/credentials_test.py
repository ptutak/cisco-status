from cisco_status.credentials import parse_router_credentials


def test_parse_credentials():
    credentials = parse_router_credentials(r"CE1,some-host,my_username,my_password")
    assert credentials.host == "some-host"
    assert credentials.name == "CE1"
    assert credentials.username == "my_username"
    assert credentials.password == "my_password"
