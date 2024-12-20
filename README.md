# Proto Chango

Test project for learning about protocol buffers

## Developer Setup

This project uses [uv](https://docs.astral.sh/uv/ "UV Documentation") for dependency management, command running, etc... install it:

```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Makefile

* ``make env`` Sets up a new virtual environment in the folder ``.venv``
* ``make compile-proto`` Run the protobuf compilter and produce ``_pb2.py`` output files
* ``make test`` Run the unittests
* ``make qt`` Quick Test invoke - like ``make test`` but doesn't run the environment setup first
* ``make sync`` Installs the project and dependencies in the local virtual environment (normally implicitly run by other targets)
* ``make check-all`` Run all code formatters, linters, tests, security scans, etc...
* ``make git-clean`` Runs the git ``fsck`` tool, prunes the reflog, etc...
