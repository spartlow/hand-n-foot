# Architecture Overview

This document captures the high-level architecture for the Hand & Foot project and where responsibilities live.

Goals
- Keep the core game engine small, deterministic, and well-tested.
- Provide a strategy API that can plug in deterministic or probabilistic player agents.
- Keep I/O (UI, CLI, web) separated from game logic to make simulations fast and headless.

Major components
- `handnfoot/` — core Python package. Contains game model, rules, scoring, and a light runner.
  - `cardtable.py` — data structures: piles, melds, players, deck operations.
  - `handnfoot.py` — CLI/prototype runner.
- `tests/` — unit tests and integration tests for the engine.
- `docs/` — user-facing documentation (rules, player guides, how-to-play).
- `_context/` — developer-only artifacts: ADRs, architecture notes, design decisions, and prioritized TODOs.

Extension points
- Strategy interface: agents implement a small API (decide melds, draws, discards, and when to go out).
- Simulation harness: runs many games headless and aggregates results to CSV/JSON.
- UI adapters: small wrappers that translate player input to strategy calls.

Non-functional concerns
- Determinism: engine operations should be seedable for reproducible simulations.
- Performance: simulation harness will avoid unnecessary allocations and I/O.
- Testability: core logic should be pure where practical and covered with tests.

Where ADRs live
- See `_context/ADRS/` for recorded Architecture Decision Records. Use incremental numbering and clear problem/decision/rationale.
