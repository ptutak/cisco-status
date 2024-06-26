from cisco_status.cli import hello


def test_hello():
    assert hello() == "Hello World"
