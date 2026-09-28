# Agents Onboarding & Context

Purpose
- Give automated assistants, new contributors, and chat sessions a short set of pointers so they immediately understand where to find architecture, decisions, and player docs.

Primary documents
- Repository overview: `README.md`
- Developer / architecture context: `_context/ARCHITECTURE.md`
- Roadmap / prioritized items: `_context/TODO.md`
- Architecture Decision Records: `_context/ADRS/` (incrementing files; add a new ADR for important decisions)
- Player-facing docs: `docs/` (`rules.md`, `player_guide.md`, `simulations.md`)
- Engine entry points: `handnfoot/handnfoot.py`, `handnfoot/cardtable.py`
- Tests: `tests/` (run `pytest -q`)

When a chat or agent session starts
- Read `README.md` for high-level goals and quick-start commands.
- Read `_context/ARCHITECTURE.md` to learn the core component responsibilities and invariants (e.g., keep logic deterministic and seedable).
- Check `_context/TODO.md` for priority work and phases.
- Inspect `_context/ADRS/` to avoid repeating past design tradeoffs; create an ADR when a decision affects architecture or public APIs.

Where to record work
- Small tasks and bugs: open an issue on the repository.
- Roadmap-level or prioritized work: update `_context/TODO.md` and reference issues.
- Significant design decisions: add an ADR under `_context/ADRS/` following the numeric naming convention (e.g., `0002-new-strategy-api.md`).

Quick commands
```bash
# Run tests
pytest -q

# Run prototype runner (may be minimal)
python -m handnfoot.handnfoot
```

Notes for strategy/simulation work
- See `docs/simulations.md` for suggested harness and outputs.
- Prefer headless, seedable simulations. Add strategy implementations in a dedicated `strategies/` package and a `tools/simulate.py` runner when ready.

If you're an agent
- Include these file paths in your context snippet when you begin a session so human reviewers can quickly follow your recommendations.
- When proposing changes to behavior, reference the relevant ADR or create one.
