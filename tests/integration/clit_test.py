from pathlib import Path

from click.testing import CliRunner

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


def test_cli(monkeypatch, tmp_path: Path):
    tmp_config_file = tmp_path / "hsrp-config.json"
    tmp_config_file.write_text(
        r"""{
    "hsrp": [
        {
            "name": "CE1",
            "group": 1,
            "state": "Active"
        },
        {
            "name": "CE1",
            "group": 2,
            "state": "Standby"
        },
        {
            "name": "CE2",
            "group": 1,
            "state": "Standby"
        },
        {
            "name": "CE2",
            "group": 2,
            "state": "Active"
        }
    ]
}"""
    )

    monkeypatch.setattr("cisco_status.cli.CiscoRouter", MyRouter)
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
        == """[
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
"""
    )
    assert result.exit_code == 0


def test_cli_fail(monkeypatch, tmp_path: Path):
    tmp_config_file = tmp_path / "hsrp-config.json"
    tmp_config_file.write_text(
        r"""{
    "hsrp": [
        {
            "name": "CE1",
            "group": 1,
            "state": "Standby"
        },
        {
            "name": "CE1",
            "group": 2,
            "state": "Standby"
        },
        {
            "name": "CE2",
            "group": 1,
            "state": "Active"
        },
        {
            "name": "CE2",
            "group": 2,
            "state": "Active"
        }
    ]
}"""
    )

    monkeypatch.setattr("cisco_status.cli.CiscoRouter", MyRouter)
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
        == """[
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
        "status": "Pass"
      }
    ]
  }
]
"""
    )
    assert result.exit_code == 0
