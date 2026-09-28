import pytest

from context import cardtable
from context import handnfoot


@pytest.fixture(autouse=True)
def reset_cardtable_modifiers():
    old_meld_method = cardtable.Modifiers.meld_method
    old_wild_ranks = list(cardtable.Modifiers.wild_ranks)
    yield
    cardtable.Modifiers.set_meld_method(old_meld_method)
    cardtable.Modifiers.set_wild_ranks(old_wild_ranks)


def _rank_points(card):
    if card.rank == cardtable.Rank.THREE and card.get_color() == cardtable.Color.RED:
        return -300
    if card.rank == cardtable.Rank.JOKER:
        return 50
    if card.rank in {cardtable.Rank.ACE, cardtable.Rank.TWO}:
        return 20
    if card.is_face_card() or card.rank == cardtable.Rank.TEN:
        return 10
    return 5


valid_cards = []
for rank_token in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "*"]:
    for suit_token in ["H", "D", "S", "C"]:
        valid_cards.append(rank_token + suit_token)
for joker_suit in ["B", "R"]:
    valid_cards.append("*" + joker_suit)

cases = []
for idx in range(100):
    shorthand = valid_cards[idx % len(valid_cards)]
    card = cardtable.Card.parse(shorthand)
    cardtable.Modifiers.set_wild_ranks([cardtable.Rank.TWO, cardtable.Rank.JOKER])
    expected_points = _rank_points(card)
    expected_meld = "WILD" if card.is_wild() else card.rank.get_shorthand()
    cases.append((shorthand, expected_points, expected_meld))


@pytest.mark.parametrize("shorthand, expected_points, expected_meld", cases)
def test_card_parsing_and_scoring_matrix(shorthand, expected_points, expected_meld):
    card = cardtable.Card.parse(shorthand)
    cardtable.Modifiers.set_wild_ranks([cardtable.Rank.TWO, cardtable.Rank.JOKER])

    game = handnfoot.HNFGame()
    assert game.get_card_points(card) == expected_points
    assert card.get_meld_type(method=cardtable.Meld.RANK) == expected_meld
    assert card.get_shorthand() == shorthand
