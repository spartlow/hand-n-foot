# Hand & Foot (family variant)

Repository for a Python implementation and simulator of the family's variant of the card game "Hand and Foot".

Purpose
- Provide a clean, testable core game engine representing hands, melds, scoring, and rules.
- Enable large-scale simulations of strategy variations and evaluation.
- Offer a user-facing layer (CLI and lightweight UI) for human play and exploration.

Status
- Prototype code lives in the `handnfoot/` package.
- Unit tests are under `tests/`.

Quick start

1. Create & activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/Scripts/activate || source .venv/bin/activate
```
2. Install dependencies (there may be none):
```bash
pip install -r requirements.txt || true
```
3. Run tests:
```bash
pytest -q
```
4. Run a prototype CLI (if available):
```bash
python -m handnfoot.handnfoot
```

Docs and internal context
- Player-facing docs: `docs/` — rules, player guides, how-to-play and examples.
- Developer/internal docs: `_context/` — architecture notes, ADRs, and implementation TODOs.

Contributing
- Open an issue describing the feature or bug.
- Keep changes small and include tests for core logic.
- Use `_context/` for architecture discussions and ADRs.

Planned phases (short)
1. Stabilize and increase test coverage for core engine.
2. Add a strategy API and baseline AI strategies.
3. Add simulation tooling and basic aggregation/visualization.
4. Implement a simple web/desktop UI for human play.

Files you may want to edit
- `handnfoot/handnfoot.py` — prototype runner
- `handnfoot/cardtable.py` — core game structures
- `tests/` — unit tests; update or add tests when changing behavior

See `_context/` and `docs/` for design notes and player help.
