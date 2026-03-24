# AGENTS.md

> Quick reference for AI coding agents.

## Project


- **Type**: CLI (Typer)

- **Language**: Python 3.10+
- **Package manager**: [uv](https://docs.astral.sh/uv/)

## Entry Points


- `high_itemset_mining/main.py` — CLI entry point


## Commands

Run `make help` for all commands. Key ones:

```
make install   # Install deps + pre-commit hooks
make check     # Lint, format, type-check
make test      # Run pytest

```

## Key Files

- `Makefile` — Project commands
- `pyproject.toml` — Dependencies and build config
- `ruff.toml` — Linter/formatter rules

- `tests/` — Test suite (pytest)
