from pathlib import Path

from click.testing import CliRunner
from pytest import fixture

from cisco_status.cli import RouterCredentials, cli


class MyRouter:
    def __init__(self, creds: RouterCredentials):
        self._creds = creds
        if self._creds.name == "CE1":
            assert self._creds.host == "host-1"
            assert self._creds.username == "username-1"
            assert self._creds.password == "password-1"
        if self._creds.name == "CE2":
            assert self._creds.host == "host-2"
            assert self._creds.username == "username-2"
            assert self._creds.password == "password-2"

    def show_standby_brief(self):
        if self._creds.name == "CE1":
            return """Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    110 P Active  local           82.0.0.3        82.0.0.1
Gi0/0/1     2    105 P Standby 82.0.0.11       local           82.0.0.9
"""
        if self._creds.name == "CE2":
            return """Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    105 P Standby 82.0.0.2        local           82.0.0.1
Gi0/0/1     2    110 P Active  local           82.0.0.10       82.0.0.9
"""
        return ""

    @classmethod
    def from_credentials(cls, creds: RouterCredentials):
        return MyRouter(creds)


@fixture
def mock_cisco_router(monkeypatch):
    monkeypatch.setattr("cisco_status.cli.CiscoRouter", MyRouter)


def test_cli(mock_cisco_router, tmp_path: Path):
    tmp_config_file = tmp_path / "hsrp-config.json"
    tmp_config_file.write_text(
        r"""{
    "hsrp": [
        {
            "CE1": [
                {
                    "group": 1,
                    "state": "Active",
                    "interface": "Gi0/0/1"
                },
                {
                    "group": 2,
                    "state": "Standby"
                }
            ]
        },
        {
            "CE2": [
                {
                    "group": 1,
                    "state": "Standby"
                },
                {
                    "group": 2,
                    "state": "Active"
                }
            ]
        }
    ]
}"""
    )

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "hsrp-status",
            "--hsrp-config-file",
            tmp_config_file.as_posix(),
            "--router-credentials",
            "CE1,host-1,username-1,password-1",
            "--router-credentials",
            "CE2,host-2,username-2,password-2",
        ],
    )
    assert (
        result.output
        == """{
  "hsrp": [
    {
      "CE1": [
        {
          "group": "Group 1",
          "status": "Pass"
        },
        {
          "group": "Group 2",
          "status": "Pass"
        }
      ]
    },
    {
      "CE2": [
        {
          "group": "Group 1",
          "status": "Pass"
        },
        {
          "group": "Group 2",
          "status": "Pass"
        }
      ]
    }
  ]
}
"""
    )
    assert result.exit_code == 0


def test_cli_fail(mock_cisco_router, tmp_path: Path):
    tmp_config_file = tmp_path / "hsrp-config.json"
    tmp_config_file.write_text(
        r"""{
    "hsrp": [
        {
            "CE1": [
                {
                    "group": 1,
                    "state": "Standby"
                },
                {
                    "group": 2,
                    "state": "Standby"
                }
            ]
        },
        {
            "CE2": [
                {
                    "group": 1,
                    "state": "Active"
                },
                {
                    "group": 2,
                    "state": "Active",
                    "interface": "Gi0/0/2"
                }
            ]
        }
    ]
}"""
    )

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "hsrp-status",
            "--hsrp-config-file",
            tmp_config_file.as_posix(),
            "--router-credentials",
            "CE1,host-1,username-1,password-1",
            "--router-credentials",
            "CE2,host-2,username-2,password-2",
        ],
    )
    assert (
        result.output
        == """{
  "hsrp": [
    {
      "CE1": [
        {
          "group": "Group 1",
          "status": "Fail - No longer Standby"
        },
        {
          "group": "Group 2",
          "status": "Pass"
        }
      ]
    },
    {
      "CE2": [
        {
          "group": "Group 1",
          "status": "Fail - No longer Active"
        },
        {
          "group": "Group 2",
          "status": "Fail - No longer Active"
        }
      ]
    }
  ]
}
"""
    )
    assert result.exit_code == 0


def test_cli_fail_parse(mock_cisco_router, tmp_path: Path):
    tmp_config_file = tmp_path / "hsrp-config.json"
    tmp_config_file.write_text(
        r"""{
    "hsrp": ""
}"""
    )

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "hsrp-status",
            "--hsrp-config-file",
            tmp_config_file.as_posix(),
            "--router-credentials",
            "CE1,host-1,username-1,password-1",
            "--router-credentials",
            "CE2,host-2,username-2,password-2",
        ],
    )

    assert result.exit_code == 1
    assert str(result.exception) == "Router: CE1 has no desired state."
