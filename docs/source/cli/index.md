# Command Line Interface (CLI)

The `qosst-core` package is shipped with a Command Line Interface (CLI) to execute some common commands to Alice and Bob.

The extended CLI documentation is available [here](./documentation.md) and the API documentation of the CLI is available [here](./api.md).

## Get help

You can get help with the `-h` or `--help` flag:

```{command-output} qosst -h
```

This displays the available command. You can also get help on a specific command:

```{command-output} qosst info -h
```

or on subcommands 

```{command-output} qosst configuration -h
```

or on command of subcommands

```{command-output} qosst configuration create -h
```

## Get the version

You can get the version of the script (which is the same as the version of the `qosst-core` package) with the `--version` flag:

```{command-output} qosst --version
```

You can get the versions of all QOSST packages with the `info` subcommand:

```{command-output} qosst info
```

## Useful commands

All commands are somehow useful, but here are the one you will probably use:

### qosst info

The `qosst info` command displays the version of the currently installed QOSST softwares.

```{command-output} qosst info
```

### qosst configuration create

The `qosst configuration create` allows to create a default configuration file. By default it will copy it to `config.toml` but you can override this location with the flag `-f`:

```{command-output} qosst configuration create -h
```

### qosst auth

If you plan to enable authentication, you might use the `qosst auth` subcommand. In particular, you can generate keys for the falcon algorithm with the `qosst auth generate-falcon` command:


```{command-output} qosst auth generate-falcon -h
```
