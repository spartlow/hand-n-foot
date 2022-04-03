import logging

from handnfoot import cardtable

def test_card_names():
    card = cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES)
    assert str(card) == "ACE of SPADES"
    assert card.get_shorthand() == "AS"

def test_meld_RankColor():
    hand = cardtable.Hand()
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES))
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.CLUBS))
    #group.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.HEARTS))
    #group.push(cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.HEARTS))
    meld = cardtable.Meld(method = cardtable.Meld.RANKCOLOR, cards = hand.cards)
    assert meld.method == cardtable.Meld.RANKCOLOR
    assert str(meld) == "[ACE of SPADES, ACE of CLUBS]"
    assert meld[0].get_meld_type(method = cardtable.Meld.RANKCOLOR) == "ABLACK"
    assert meld.get_type() == "ABLACK"
