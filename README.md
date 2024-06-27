# cisco-status
I assumed that we have a desired state of the cisco router configuration. This package is used to check the current state of the cisco router configuration and compare it with the desired state. The package will return the differences between the current state and the desired state.
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

```bash
python -m cisco_status.cli --help
```


## development

To install the package in development mode, run the following command:

```bash
make install-dev
```
