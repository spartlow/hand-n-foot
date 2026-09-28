RULES_CUSTOMIZATIONS.md

Purpose
- This file lists customization points and implementation suggestions to make the Hand & Foot engine configurable for different house-rule variants.

Suggested customization options

- Pack count policy
  - Option A (current): `players + 1` packs.
  - Option B: fixed "decks per pair" (e.g., 2 decks per pair). Implement by adding a config parameter `decks_per_pair` and computing total packs = ceil(players/2) * decks_per_pair * (1 pair?) or another mapping.

- Wild configuration
  - Make wild ranks configurable (default: Twos and Jokers). Expose via `HNFRules` initializer or a configuration object and use `cardtable.Modifiers.set_wild_ranks()` at startup.
  - Toggle wild-only melds: a boolean flag `allow_melds_of_wilds` (already present in `HNFRules` but currently unused for enforcement in some code paths).
  - Allow adding wilds to completed piles: boolean `allow_add_wilds_to_existing_piles` and enforce in `add_fans_to_piles` and related methods.

- Meld method
  - Support `Meld.RANK` (current) and `Meld.RANKCOLOR` via config. Expose `Modifiers.set_meld_method()` based on configuration.

- Opening thresholds
  - Make opening requirements per round configurable (array or callable). Replace `HNFRules.round_starting_points()` with values loaded from config.

- Red three behavior
  - Make red-three handling configurable (bonus, penalty, special placement rules). Expose in `HNFRules` and use `get_card_points()` logic accordingly.

- Discard-to-end behavior
  - Expose `allow_discard_to_end_last_round` and/or more fine-grained controls. Ensure enforcement is added to `play_turn()` logic (the repository now has a basic enforcement for the final round; consider making the rule configurable by round index or boolean flags).

- Completed pile thresholds & bonuses
  - Make `MIN_PILE_SIZE` configurable and allow `pure` vs `dirty` bonus values to be set by config.

- AI / Strategy exposure
  - Expose strategy parameters via configuration to preview different play styles.

Implementation notes
- Add a `config` module or small YAML/JSON loader consumed by `HNFGame.__init__` to set the options above. Keep backward compatibility with current defaults.
- Unit tests: add test parametrization to cover a couple common alternate rulesets (e.g., "twos are wild" vs "twos not wild").
- CLI: expose a `--rules` flag to load a JSON rules file for quick experimentation.

Small, incremental path to implement
1. Add a `RulesConfig` dataclass in `handnfoot/handnfoot.py` and pass it into `HNFGame.__init__` (defaults to current behavior).
2. Wire `RulesConfig` fields through to `HNFRules` and `cardtable.Modifiers` during `game_setup()`.
3. Add tests that instantiate `HNFGame` with a custom `RulesConfig` and assert behavior (e.g., wild ranks, opening thresholds).

If you'd like I can implement any of the items above; say which ones and I'll add the config plumbing and tests.
