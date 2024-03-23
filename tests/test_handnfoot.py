#!/usr/bin/env python

import os
import sys
import logging
import pytest

from context import handnfoot
from context import cardtable
#from handnfoot import cardtable

def test_card_points():
    rules = handnfoot.HNFRules()
    assert rules.get_card_points(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES)) == 20
    assert rules.get_card_points(cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.HEARTS)) == 20
    assert rules.get_card_points(cardtable.Card(cardtable.Rank.FIVE, cardtable.Suit.SPADES)) == 5
    assert rules.get_card_points(cardtable.Card(cardtable.Rank.THREE, cardtable.Suit.SPADES)) == 5
    assert rules.get_card_points(cardtable.Card(cardtable.Rank.THREE, cardtable.Suit.HEARTS)) == -300
    assert rules.get_card_points(cardtable.Card(cardtable.Rank.JOKER, cardtable.Suit.RED)) == 50

def test_card_is_wild():
    rules = handnfoot.HNFRules()
    assert rules.card_is_wild(cardtable.Card(cardtable.Rank.JOKER, cardtable.Suit.RED)) == True
    assert rules.card_is_wild(cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.SPADES)) == True
    assert rules.card_is_wild(cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.HEARTS)) == True
    assert rules.card_is_wild(cardtable.Card(cardtable.Rank.THREE, cardtable.Suit.DIAMONDS)) == False
    assert rules.card_is_wild(cardtable.Card(cardtable.Rank.KING, cardtable.Suit.CLUBS)) == False
    assert rules.card_is_wild(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.HEARTS)) == False

if __name__ == "__main__":
    pytest.main([__file__])
