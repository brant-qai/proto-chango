# A few tol-level variables
ENV_DIR := .venv
PIP_CMD := pip --no-input
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(patsubst %/,%,$(dir $(MAKEFILE_PATH)))

# Define a value to use for newlines
define newline


endef

ifeq (, $(shell command -v protoc))
$(warning $(newline)WARNING: No protoc command found on PATH; some Makefile targes will not work as expected.$(newline))
endif

all: format-code test artifacts

$(ENV_DIR)/bin/activate:
	uv sync --all-extras

.PHONY: env
env: $(ENV_DIR)/bin/activate

# Sync the virtual environment regardless of whether it exists
.PHONY: sync
sync:
	@uv sync --all-extras --locked

# Alias for muscle memory; I got too used to typing "make build"
.PHONY: build
build: sync

.PHONY: update-lockfile
update-lockfile:
	@uv sync --all-extras --all-packages

.PHONY: unittests
unittests:
	@uv run python -Wd -m unittest discover -t . --verbose --locals --buffer

# Shorthand alias for running unittests
.PHONY: qt
qt: unittests

.PHONY: test
test: build check-code mypy qt

.PHONY: artifacts
artifacts: wheel

.PHONY: wheel
wheel: sync
	@uv run python -m build --wheel .

$(MAKEFILE_DIR)/src/models.py:

.PHONY: compile-proto
compile-proto: $(MAKEFILE_DIR)/src/models.py
	protoc --proto_path=$(MAKEFILE_DIR)/src/proto_chango --python_out=$(MAKEFILE_DIR)/src/proto_chango $(MAKEFILE_DIR)/src/proto_chango/models.proto
	- @uv run ruff check --fix-only $(MAKEFILE_DIR)/src/proto_chango/*_pb2.py
	- @uv run ruff format $(MAKEFILE_DIR)/src/proto_chango/*_pb2.py

.PHONY: format-code
format-code: $(ENV_DIR)
	@uv run ruff check --fix-only src/ tests/
	@uv run ruff format src/ tests/

.PHONY: check-code
check-code: $(ENV_DIR) check-ruff

.PHONY: check-ruff
check-ruff:
	@uv run ruff check src/ tests/

.PHONY: freeze
freeze: env
	- @uv pip freeze --color auto

shell: env
	- @uv run python

.PHONY: mypy
mypy:
	@uv run mypy src/

.PHONY: pyright
pyright:
	@uv run pyright src/

.PHONY: check-types
check-types: $(ENV_DIR) mypy pyright

# Formats code, runs all checks and tests (except compiled code test)
.PHONY: check-all
check-all: sync format-code check-ruff mypy pyright qt bandit

.PHONY: clean
clean:
	- @rm -rf build/
	- @git clean -fX >> /dev/null 2>&1

.PHONY: env-clean
env-clean: clean
	- @git clean -dfX >> /dev/null 2>&1
	- @rm -rf $(ENV_DIR)
	- @rm -rf .env*
	- @rm -rf .venv*

.PHONY: git-clean
git-clean: clean
	- @git fsck
	- @git reflog expire --expire=now --all
	- @git repack -ad
	- @git prune
