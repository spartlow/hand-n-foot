#!/usr/bin/env python

import os
import sys
import logging
import pytest

from context import cardtable
#from handnfoot import cardtable

def test_card_names():
    card = cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES)
    assert str(card) == "ACE of SPADES"
    assert card.get_shorthand() == "AS"
    card2 = cardtable.Card.parse("5H")
    assert str(card2) == "FIVE of HEARTS"

def test_meld_Rank():
    method = cardtable.Meld.RANK
    hand = cardtable.Hand()
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES))
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.CLUBS))
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.HEARTS))
    meld = cardtable.Meld(method = method, cards = hand.cards)
    assert meld.method == method
    assert str(meld) == "[ACE of SPADES, ACE of CLUBS, ACE of HEARTS]"
    assert meld[0].get_meld_type(method = method) == "A"
    assert meld.get_type() == "A"
    hand.push(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.HEARTS))
    hand.push(cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.HEARTS))
    melds = cardtable.Meld.get_melds(cards = hand.cards, method = method)
    assert len(melds) == 2
    assert melds[0].get_type() == "A"
    assert melds[1].get_type() == "2"

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

def test_includes_meld():
    # Setup
    method = cardtable.Meld.RANKCOLOR
    cards = [cardtable.Card.parse("4H"),
        cardtable.Card.parse("9S"),
        cardtable.Card.parse("JD"),
        cardtable.Card.parse("9C")]
    similar = [cardtable.Card.parse("4D"),
        cardtable.Card.parse("JH")]
    dissimilar = [cardtable.Card.parse("2H"),
        cardtable.Card.parse("9H"),
        cardtable.Card.parse("JC")]
    hand = cardtable.Hand(cards = cards)

    # Test CardGroup includes_meld_type
    for card in cards:
        meld_type = meld_type = card.get_meld_type(method = method)
        assert hand.includes_meld_type(meld_type = meld_type, method = method)
    for card in similar:
        meld_type = meld_type = card.get_meld_type(method = method)
        assert hand.includes_meld_type(meld_type = meld_type, method = method)
    for card in dissimilar:
        meld_type = meld_type = card.get_meld_type(method = method)
        assert not hand.includes_meld_type(meld_type = meld_type, method = method)

    # Test PlayingArea includes_meld_type
    cards2 = [cardtable.Card.parse("5C")]
    pile = cardtable.Pile(cards = cards2)
    empty_pile = cardtable.Pile()
    area = cardtable.PlayingArea(name="TestArea", groups = [hand, pile, empty_pile])
    for card in cards:
        meld_type = meld_type = card.get_meld_type(method = method)
        assert area.includes_meld_type(meld_type = meld_type, method = method)
    for card in cards2:
        meld_type = meld_type = card.get_meld_type(method = method)
        assert area.includes_meld_type(meld_type = meld_type, method = method)
    for card in dissimilar:
        meld_type = meld_type = card.get_meld_type(method = method)
        assert not area.includes_meld_type(meld_type = meld_type, method = method)

if __name__ == "__main__":
    pytest.main([__file__])
