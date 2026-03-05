# Handoff

## Current State

- GUI app entrypoint: `nummer_gen_plb_2021.py` (PyQt5).
- Environment management migrated to `uv`.
- Dependencies are defined in `pyproject.toml` and locked in `uv.lock`.

## Setup

1. Install `uv` (https://docs.astral.sh/uv/).
2. From repo root, run:
   - `uv sync --dev`

## Run

- Start the app:
  - `uv run python nummer_gen_plb_2021.py`
- Run tests:
  - `uv run pytest -q`

## Notes

- Settings loading supports both JSON and legacy pickle files.
- Use only trusted pickle files.
- Some existing tests currently fail due pre-existing test/code mismatches, not because of the `uv` migration.
