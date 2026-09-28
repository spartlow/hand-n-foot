# Implementation TODOs and Phases

Short-term (now)
- Stabilize core game behavior and expand unit tests to cover edge-cases.
- Add seedable RNG to the engine for reproducible simulations.
- Add `docs/` rules and player guide pages.

Medium-term
- Design and implement a Strategy API for pluggable player agents.
- Provide a simulation harness to run many games and export results.
- Add basic CLI tools for running simulations and analyzing results.

Long-term
- Create a web UI or desktop wrapper for interactive human play.
- Add a metrics/dashboard system for visualizing simulation outputs.
- Explore reinforcement learning or evolutionary search to discover high-performing strategies.

Notes
- Keep `_context/ADRS/` for decisions worth preserving (tradeoffs, changed behavior).
- Use issues for day-to-day tasks and keep `_context/TODO.md` for roadmap-level items.
