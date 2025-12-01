#!/usr/bin/env python

import os
import sys
import logging
import pytest

from context import handnfoot
from context import cardtable
#from handnfoot import cardtable

def test_card_points():
    game = handnfoot.HNFGame()
    assert game.get_card_points(cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.SPADES)) == 20
    assert game.get_card_points(cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.HEARTS)) == 20
    assert game.get_card_points(cardtable.Card(cardtable.Rank.FIVE, cardtable.Suit.SPADES)) == 5
    assert game.get_card_points(cardtable.Card(cardtable.Rank.THREE, cardtable.Suit.SPADES)) == 5
    assert game.get_card_points(cardtable.Card(cardtable.Rank.THREE, cardtable.Suit.HEARTS)) == -300
    assert game.get_card_points(cardtable.Card(cardtable.Rank.JOKER, cardtable.Suit.RED)) == 50

def test_card_is_wild():
    rules = handnfoot.HNFRules()
    assert (cardtable.Card(cardtable.Rank.JOKER, cardtable.Suit.RED)).is_wild() == True
    assert (cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.SPADES)).is_wild() == True
    assert (cardtable.Card(cardtable.Rank.TWO, cardtable.Suit.HEARTS)).is_wild() == True
    assert (cardtable.Card(cardtable.Rank.THREE, cardtable.Suit.DIAMONDS)).is_wild() == False
    assert (cardtable.Card(cardtable.Rank.KING, cardtable.Suit.CLUBS)).is_wild() == False
    assert (cardtable.Card(cardtable.Rank.ACE, cardtable.Suit.HEARTS)).is_wild() == False

def test_get_card_desirability():
    game = handnfoot.HNFGame()
    player = cardtable.Player("J", precision=5, speed=1.2)
    strategy = handnfoot.Strategy()
    game.add_player(player, strategy)
    game.start()
    cp = cardtable.Card.parse
    player.get_area("complete").append(cardtable.Pile(cards = [cp("5S"), cp("5C"), cp("5D"), cp("5S"), cp("5H"), cp("5D"), cp("5S"), cp("5C"), cp("5D")]))
    player.get_area("down").append(cardtable.Pile(cards = [cp("6S"), cp("6C"), cp("6D"), cp("6S"), cp("6D")]))
    player.get_hand().add([cp("7H"), cp("7H"), cp("7D"), cp("7S")])
    assert (strategy.get_card_desirability(cp("5H"), player) < strategy.get_card_desirability(cp("7C"), player))
    assert (strategy.get_card_desirability(cp("8H"), player) < strategy.get_card_desirability(cp("5H"), player))
    assert (strategy.get_card_desirability(cp("8H"), player) == strategy.get_card_desirability(cp("9H"), player))
    assert (strategy.get_card_desirability(cp("9H"), player) < strategy.get_card_desirability(cp("AH"), player))

def test_sort_by_desirability():
    game = handnfoot.HNFGame()
    player = cardtable.Player("J", precision=5, speed=1.2)
    strategy = handnfoot.Strategy()
    game.add_player(player, strategy)
    game.start()
    cp = cardtable.Card.parse
    player.get_area("complete").append(cardtable.Pile(cards = [cp("5S"), cp("5C"), cp("5D"), cp("5S"), cp("5H"), cp("5D"), cp("5S"), cp("5C"), cp("5D")]))
    player.get_area("down").append(cardtable.Pile(cards = [cp("6S"), cp("6C"), cp("6D"), cp("6S"), cp("6D")]))
    player.get_hand().add([cp("7H"), cp("7H"), cp("7D"), cp("7S")])
    cards = [cp("5H"), cp("8H"), cp("9H"), cp("AH"), cp("7C"), cp("6C"), cp("2D")]
    sorted_cards = strategy.sort_by_desirability(cards, player)
    expected = [cp("6C"), cp("7C"), cp("2D"), cp("5H"), cp("AH"), cp("8H"), cp("9H")]
    print(sorted_cards)
    assert cardtable.cards_to_str(sorted_cards) == cardtable.cards_to_str(expected)

if __name__ == "__main__":
    pytest.main([__file__])
