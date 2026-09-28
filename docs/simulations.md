# Simulations (starter)

This page explains the intended simulation workflow for running many games to evaluate strategies.

Design
- Simulations should run headless (no UI) and be seedable for reproducibility.
- Each strategy implements a small API so the harness can swap agents easily.

Suggested CLI (future)
- `python -m tools.simulate --strategies baseline,greedy --games 1000 --seed 42 --out results.csv`

Output
- Export aggregated metrics to CSV/JSON: wins, average score, distribution of melds, time-per-game.

Next steps
- Add a `tools/` simulation runner and a `strategies/` package with baseline agents.
