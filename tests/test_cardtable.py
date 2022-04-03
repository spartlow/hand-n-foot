import logging

from handnfoot import cardtable

def test_card_names():
    card = cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES)
    assert str(card) == "ACE of SPADES"
    assert card.get_shorthand() == "AS"
    card2 = cardtable.Card.parse("5H")
    assert str(card2) == "FIVE of HEARTS"

def test_meld_RankColor():
    method = cardtable.Meld.RANKCOLOR
    hand = cardtable.Hand()
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES))
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.CLUBS))
    meld = cardtable.Meld(method = method, cards = hand.cards)
    assert meld.method == method
    assert str(meld) == "[ACE of SPADES, ACE of CLUBS]"
    assert meld[0].get_meld_type(method = method) == "ABLACK"
    assert meld.get_type() == "ABLACK"
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.HEARTS))
    hand.push(cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.HEARTS))
    melds = cardtable.Meld.get_melds(cards = hand.cards, method = method)
    assert len(melds) == 3
    assert melds[0].get_type() == "ABLACK"
    assert melds[1].get_type() == "ARED"
    assert melds[2].get_type() == "2RED"
