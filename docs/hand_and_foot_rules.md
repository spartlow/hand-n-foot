Hand & Foot — Rules (summary)

This document gives a short, user-friendly summary of common "Hand and Foot" rules (based on common sources such as Bicycle's how-to guide), then lists how the current code in `handnfoot/` implements or differs from those rules. Use this as a reference and tweak the "House Rules" questions at the end to capture your family's variants.

**1. Objective**
- The goal is to form melds (sets) of like-ranked cards, create completed piles, and score points. Play through a fixed number of rounds, scoring each round and totaling at the end.

**2. Players & Teams**
- Typically played with 2–6 players. Players often form teams of two, but the code treats players individually and can be adapted for teams.

Hand & Foot — Rules (official for this version)

This document gives a concise, user-friendly summary of the rules that are the official defaults for this codebase (based on common references such as Bicycle's how-to guide). It also notes a few implementation details and assumptions.
**3. Cards & Decks**
- Melds are formed by rank (e.g., a set of Kings) and may be "clean" (no wilds) or "dirty" (containing wild cards).
 Use multiple standard 52-card decks plus jokers. This implementation uses `number_of_players + 1` packs by default (i.e., one pack per player plus one extra).
**4. Wild Cards**
 Wild cards: Twos and Jokers are wild. Wild-only melds are NOT allowed. Wilds cannot be added to a completed dirty pile (completed piles marked dirty cannot accept wilds). Dirty melds much have more non-wild cards as wild cards.
 Wilds substitute for natural cards subject to the rules above; the implementation enforces these restrictions by default.

 Basic meld: at least 3 natural cards of the same rank.
 Once a meld (fan) reaches the minimum pile size of 7 cards it can be moved to a completed pile.
 Completed piles are classified as `pure` (no wilds) or `dirty` (contain wilds). Pure piles earn +300 bonus points; dirty piles earn +100 bonus points.
-- Scoring examples:
-- Completed piles: pure pile bonus is higher than dirty pile bonus (+300 pure / +100 dirty).
- Before a player/team may lay down, they must meet a minimum-point requirement based on the round (commonly escalating each round). Typical example: Round 1 = 50 points, Round 2 = 75, Round 3 = 100, Round 4 = 150. The implementation uses these exact thresholds.
 Wild-only melds: wild-only melds are not allowed.
 Red Threes: Red threes are always a penalty.
 Only the last round requires that a player go out without using a discard to end the round (i.e., discarding to end the final round is not allowed). In other rounds, a player may end the round by discarding their last card.
- Once a meld (fan) reaches a configured minimum pile size (commonly 7), it can be moved to a completed pile and remain open for others to add to.
**9. Scoring**
  - Aces & Twos = 20 points
  - Face cards (J/Q/K) & Tens = 10 points
  - Number cards (4–9 etc.) = 5 points
  - Red Threes: treated specially (code treats red 3 as -300 if in hand; see notes below)
- Completed piles: clean pile bonus is higher than dirty pile bonus (implementation: +300 if pure, else +100).
- Points for unplayed cards in hand/foot are subtracted from a player's score.


Implementation notes (what the code does)
- Wild cards: `cardtable.Modifiers.set_wild_ranks([Rank.TWO, Rank.JOKER])` — Twos and Jokers are wilds.
- Meld method: `cardtable.Modifiers.set_meld_method(cardtable.Meld.RANK)` — melds are determined by rank only (not color).
- Round opening thresholds: `HNFRules.round_starting_points`: [50, 75, 100, 150] for rounds 1–4.
- Pack/deck handling: the code builds a `Pack` (one 54-card pack including two jokers). At `game_setup()` the code creates `len(players) + 1` packs and combines/shuffles them for play.
- Dealing: the implementation deals each player two separate 11-card piles (one to be the hand, one to be the foot) using a particular distribution: each player receives one 11-card pile taken from the previous player's draw pile and one from the next player's draw pile — then randomly assigns which becomes hand versus foot. Practically: players end up with 11-card hand and 11-card foot.
- Draw mechanics: players draw until they have drawn 2 cards on their draw action (the code's `draw()` pulls 2 cards total per draw).
- Minimum pile size to convert a fan to a completed pile: `MIN_PILE_SIZE = 7`.
- Laying down: only non-wild melds are considered for initial lay unless the rules specifically allow wild-only melds. The code queues up melds of 3+ non-wilds for laying; once laid, `add_fans_to_piles` will convert fans to completed piles if they reach the MIN_PILE_SIZE.
- Wild handling while down: code tries to use wilds to extend pairs into melds or fill deficits in dirty piles, subject to internal rules (e.g., `allow_add_wilds_to_existing_piles` is present in `HNFRules` but defaults to False).
- Red Threes: The scoring function treats a red three specifically — `get_card_points` returns -300 for red threes in hand (and tests reference the special behavior)—this is a code-specific choice worth verifying against your house rules.
- Completed pile bonuses: in `get_player_score`, piles with `pile.hnf_pure == True` get +300, otherwise +100.

Differences vs. common Bicycle-style rules (observed)
- Number of decks: common guidance is decks per pair; the code uses `(number of players) + 1` packs. That may produce a different deck count than your usual house practice.
- Dealing algorithm: code uses neighboring draw piles and a random choice to assign which of the two 11-card piles becomes the player's foot. This is a particular implementation detail that is different from some manuals that simply deal sequentially.
- Red Threes handling: standard variants often give bonuses for red threes; the code treats red threes specially (heavily penalizing them in hand with -300). Make sure this matches what you expect.
- Wilds and piles: `allow_add_wilds_to_existing_piles` is False by default — some rules allow adding wilds freely to existing piles.
- Wild-only melds: `allow_melds_of_wilds` is False by default in the rules object; some house rules permit wild-only melds.
- Minimum meld size: code assumes melds of size >= 3 (and `allow_melds_of_threes` True). Some variants forbid 3s or treat them specially.
- Pile (complete) bonus values and definitions: code gives a large bonus for a pure pile (+300) and smaller for dirty (+100) — confirm these numbers with your expected scoring method.

Suggested assumptions and TODOs (where code is ambiguous or has TODO comments)
- The code has a few TODOs: e.g., checks around minimum opening points when considering wilds, restrictions about adding wilds to piles, and whether discarding is allowed to end the last round. Decide these behaviors and we can implement them or change the configuration.
- The Strategy object contains heuristics for drawing and discarding which govern AI behavior in simulations; they are decoupled from core rule choices.


House-rules interview (5 short questions)
- Q1: How many decks (including jokers) do we usually play with for X players? Do you prefer the code default of `players + 1` packs or a fixed decks-per-pair rule (e.g., 2 decks per pair)?
- Q2: How do you treat red threes? (Common variants: bonus points when placed; others treat them specially). The code currently treats red threes as -300 in the hand (penalty); is that right for your family?
- Q3: Wild rules: are Twos and Jokers wild in your house rules? Are wild-only melds allowed? Can wilds be added to existing completed piles?
- Q4: Opening meld requirements by round: do you want the default `[50, 75, 100, 150]` thresholds, or do you use different values (or per-team opening rules)?
- Q5: Completed piles and bonuses: do you use a larger bonus for clean piles (no wilds) vs dirty piles? If so, what point values for clean vs dirty pile bonus would you like (the code uses +300 clean / +100 dirty)?


Next steps
- I created this draft summary in `docs/hand_and_foot_rules.md`. Tell me which of the house-rule options above reflect your family, and I will update the rules file and optionally change the code defaults to match.
- If you want, I can also implement any changes (e.g., different pack counts, different scoring for red threes, or relaxing wild rules) and run the tests.
