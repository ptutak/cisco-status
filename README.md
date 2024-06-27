# cisco-status
This package is used to check the current state of the cisco router configuration and compare it with the desired state.
The package will return the differences between the current state and the desired state.

Right now, the package only supports the following commands:
- hsrp-status

## install

To install the package, run the following command:

```bash
make install
```

or you can just install via pip:

```bash
pip install .
```

## usage

For help type the following command:
```bash
python -m cisco_status.cli --help
```

## development

To install the package in development mode, run the following command:

```bash
make install-dev
```


To run the tests, run the following command:

```bash
pytest --cov
```

Currently there are no e2e tests because of a lack of a device or a proper virtual device.

## commands

### hsrp-status
The command accepts hsrp desired configuration in the format:

Typical usage:
```bash
python -m cisco_status.cli hsrp-status -r CE1,host-1,username-1,password-1 -r CE2,host-2,username-2,password-2 -c hsrp-desired.json
```

```json
{
    "hsrp": [
        {
            "CE1": [
                {
                    "group": 1,
                    "status": "Active"
                },
                {
                    "group": 2,
                    "status": "Standby"
                }
            ]
        },
        {
            "CE2": [
                {
                    "group": 1,
                    "status": "Standby"
                },
                {
                    "group": 2,
                    "status": "Active"
                }
            ]
        }
    ]
}
```

Then it presents the result in the same format:

```json
{
    "hsrp": [
        {
            "CE1": [
                {
                    "group": "Group 1",
                    "status": "Pass",
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
                    "status": "Fail - No longer Standby"
                },
                {
                    "group": "Group 2",
                    "status": "Fail - No longer Active"
                }
            ]
        }
    ]
}
