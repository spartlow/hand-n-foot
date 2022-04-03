"""
Classes for a standard deck of cards
"""
from __future__ import annotations
import typing
import itertools
from xmlrpc.client import Boolean
import numpy as np
from enum import Enum
import random
import math
from types import SimpleNamespace

BACKS = ["B", "R", "G", "Y", "K"]
def get_next_back():
    get_next_back.back_idx += 1
    return (BACKS[get_next_back.back_idx % 2] + str(get_next_back.back_idx // 2 + 1))
get_next_back.back_idx = -1

class Color(Enum):
    RED = 1
    BLACK = 2
    def __repr__(self) -> str:
        return self.name+"!"
    def __str__(self) -> str:
        return self.name

from enum import Enum
class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4
    BLACK = 5 # For Jokers
    RED = 6 # For Jokers
    def _get_shorthands(self) -> str:
        return ["H", "D", "S", "C", "B", "R"]
    def get_shorthand(self) -> str:
        return self._get_shorthands()[self.value - 1]
    def get_color(self) -> Color:
        return [Color.RED, Color.RED, Color.BLACK, Color.BLACK, Color.BLACK, Color.RED][self.value - 1]
    def __repr__(self) -> str:
        return self.name+"!"
    def __str__(self) -> str:
        return self.name
    @classmethod
    def _shorthands(self) -> str:
        return ["H", "D", "S", "C", "B", "R"]
    @classmethod
    def parse(cls, shorthand) -> Suit:
        return cls(cls._shorthands().index(shorthand) + 1)

from enum import Enum
class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    JOKER = 14
    def _get_shorthands(self) -> str:
        return ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "*"]
    def get_shorthand(self) -> str:
        return self._get_shorthands()[self.value - 1]
    def is_face_card(self) -> Boolean:
        if self.value >= self.JACK.value and self.value <= self.KING.value: # Jokers are not considered face cards
            return True
        else:
            return False
    def __repr__(self) -> str:
        return self.name+"!"
    def __str__(self) -> str:
        return self.name
    @classmethod
    def _shorthands(self) -> str:
        return ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "*"]
    @classmethod
    def parse(cls, shorthand) -> Rank:
        return cls(cls._shorthands().index(shorthand) + 1)

"""
Defines a card
"""
class Card:
    rank = suit = back = None
    def __init__(self, rank, suit, back = ""):
        self.rank = rank
        self.suit = suit
        self.back = back
    def _parse(shorthand):
        shorthand = Suit.HEARTS
    def __repr__(self) -> str:
        return (str(self.back)+" "+str(self.rank)+" of "+str(self.suit)).strip() # +" is "+str(self.suit.get_color())
    def get_shorthand(self) -> str:
        return self.rank.get_shorthand()+self.suit.get_shorthand()
    def is_face_card(self) -> Boolean:
        return self.rank.is_face_card()
    def get_color(self) -> Color:
        return self.suit.get_color()
    def count_eyes(self) -> int:
        if self.rank == Rank.JOKER:
            return 2
        elif self.is_face_card():
            if self.get_shorthand in ["JS", "JH", "KD"]:
                return 1
            return 2
        elif self.rank == Rank.JOKER:
            return 2
        return 0
    def get_unicode(self) -> str:
        if self.suit == Suit.RED:
            if self.rank is not Rank.JOKER: raise "Unexpected rank for Suit.RED: "+self.rank
            code = int("F0BF")
        elif self.suit == Suit.BLACK:
            if self.rank is not Rank.JOKER: raise "Unexpected rank for Suit.BLACK: "+self.rank
            code = int("F0DF")
        else:
            if self.suit == Suit.SPADES:
                #code = u"\x1f0\xa0"
                code = int("1F0A0", 16)
            elif self.suit == Suit.HEARTS:
                code = int("1F0B0", 16)
            elif self.suit == Suit.DIAMONDS:
                code = int("1F0C0", 16)
            elif self.suit == Suit.CLUBS:
                code = int("1F0D0", 16)
            else: raise "Unexpected suit: "+self.suit
            if self.rank.value <= Rank.JACK.value:
                code += self.rank.value
            else:
                code += self.rank.value + 1 #skip the "Knight" card
        print(code)
        return chr(code)
    def get_meld_type(self, method) -> str:
        return Meld.get_card_meld_type(self, method)
    @classmethod
    def parse(cls, shorthand, back = "") -> Card:
        return cls(Rank.parse(shorthand[0]), Suit.parse(shorthand[1]), back)

"""
Defines a deck of cards.
For a group of cards, see Pile.
"""
class Deck:
    back = cards = None
    def __init__(self, back = None):
        if back == None:
            back = get_next_back()
        self.back = back
        self.cards = []
        for r in itertools.product([e for e in Rank], [e for e in Suit]):
            if r[0] is not Rank.JOKER and r[1] is not Suit.BLACK and r[1] is not Suit.RED:
                self.cards.append(Card(r[0], r[1], self.back))
        self.cards.append(Card(Rank.JOKER, Suit.BLACK, self.back))
        self.cards.append(Card(Rank.JOKER, Suit.RED, self.back))
        #print(self.cards)
    def get_pile(self, face_up = False) -> Pile:
        return Pile(self.cards)

class Meld(list):
    RANKCOLOR = 1
    def __init__(self, method, cards = []):
        self.method = method
        if cards:
            super(Meld, self).__init__(cards)
        else:
            super(Meld, self).__init__()
    def get_type(self) -> str:
        if len(self):
            return Meld.get_card_meld_type(card = self[0], method = self.method)
        else:
            return None
    @classmethod
    def get_card_meld_type(cls, card, method) -> str:
        if method is cls.RANKCOLOR:
            meld_type = card.rank.get_shorthand() + str(card.get_color())
        else:
            raise ValueError("Unknown method "+method)
        return meld_type
    @classmethod
    def cards_include_meld_type(cls, cards, meld_type, method) -> Boolean:
        for card in cards:
            if Meld.get_card_meld_type(card, method) == meld_type:
                return True
        return False
    @classmethod
    def get_melds(cls, cards, method) -> List['Meld']:
        if len(cards) == 0:
            return []
        melds = dict()
        for card in cards:
            meld_type = cls.get_card_meld_type(card, method)
            if meld_type not in melds:
                melds[meld_type] = Meld(method = method)
            melds[meld_type].append(card)
        return list(melds.values())


class CardGroup():
    cards = None
    def count(self) -> int:
        return len(self.cards)
    def __str__(self) -> str:
        return str(self)
    def get_melds(self, method) -> List['Meld']:
        return Meld.get_melds(cards = self.cards, method = method)
    def count_melds(self, method) -> int:
        return len(self.get_melds(method))
    def includes_meld_type(self, meld_type, method) -> Boolean:
        return Meld.cards_include_meld_type(cards = self.cards, meld_type = meld_type, method = method)
    def add(self, cards) -> None:
        if isinstance(cards, CardGroup):
            self.cards.extend(cards.cards)
            cards.cards = []
        else:
            self.cards.extend(cards)
    def push(self, card) -> None:
        self.cards.append(card)
    def pop(self) -> Card:
        return self.cards.pop()
    def sort(self, method) -> None:
        if method == Meld.RANKCOLOR:
            self.cards.sort(key=lambda card: card.rank.get_shorthand()+str(card.get_color()))
        else:
            raise "Unknown sort method: "+method
    def calc_entropy(self, method) -> float:
        # See https://stackoverflow.com/questions/19434884/determining-how-well-a-deck-is-shuffled
        if method == Meld.RANKCOLOR:
            num_sets = self.count_melds(method=method)
            print(num_sets)
            min_sets = 1 #math.ceil(self.count() / 2)
            max_sets = min(28, self.count())
            if max_sets - min_sets == 0:
                return 1.0
            return ((num_sets - min_sets) / (max_sets - min_sets))
        else:
            raise "Unknown calc_entropy method: "+str(method)

class Pile(CardGroup):
    cards = face_up = None
    PERFECT_SHUFFLE = 1
    RIFFLE_SHUFFLE = 2
    MULTI_QUICK_SHUFFLE = 3
    def __init__(self, cards = None, face_up = False):
        if cards == None: cards = list()
        self.cards = cards
        self.face_up = face_up
    def draw(self, number = 1) -> List['Card']:
        cards = []
        for _ in range(number):
            cards.append(self.pop())
        return cards
    def peek(self) -> Card:
        return self.cards[-1]
    def flip(self) -> None:
        self.face_up = not self.face_up
        self.cards.reverse()
    def deal(self, num_piles, num_cards = 1, face_up = False) -> List['Pile']:
        piles = []
        for _ in range(num_piles):
            piles.append(Pile(face_up = face_up))
        for _ in range(num_cards):
            for p_idx in range(num_piles):
                card = self.pop()
                if card == None:
                    raise "No more cards to deal!"
                #print(str(card)+" to pile "+str(p_idx))
                piles[p_idx].push(card)
        return piles
    def split(self, num_piles, face_up = False, include_current = False) -> List['Piles']:
        piles = []
        cards_list = np.array_split(self.cards, num_piles)
        for cards in cards_list:
            piles.append(Pile(cards = list(cards), face_up = face_up))
        if include_current:
            self.cards = piles[0].cards
            del piles[0]
        else:
            self.cards = []
        return piles
    def shuffle(self, iterations = 7, precision = 10, method = RIFFLE_SHUFFLE) -> None:
        if len(self.cards) > 100:
            raise "Can't shuffle that many. Specify another method."
        if method == self.PERFECT_SHUFFLE:
            random.shuffle(self.cards)
        elif method == self.RIFFLE_SHUFFLE:
            self.riffle_shuffle(iterations = iterations, precision = precision)
        elif method == self.MULTI_QUICK_SHUFFLE:
            self.multi_quick_shuffle(iterations = iterations, precision = precision)
        else:
            raise "Unknown shuffle method: "+method
    def riffle_shuffle(self, iterations = 7, precision = 10) -> None:
        if len(self.cards) > 100:
            raise "Can't riffle shuffle that many. Specify another method."
        half = [[],[]]
        if len(self.cards) < 2:
            return
        if precision > len(self.cards) / 2:
            precision = int(len(self.cards) / 2)
        for iteration in range(iterations):
            # First split the deck
            if precision == 1:
                error = 0
            else:
                error = random.randrange(0 - (precision - 1), (precision - 1), 1)
            mid_idx = int(len(self.cards) / 2) + error
            half[0] = self.cards[:mid_idx]
            half[1] = self.cards[mid_idx:]
            # Next let them fall back together
            cards = []
            side = random.randrange(0, 1, 1)
            loop_count = 0
            while len(half[0]) > 0 and len(half[1]) > 0:
                side = (side + 1) % 2
                #print(precision)
                if precision == 1:
                    count = 1
                else:
                    count = min( len(half[side]), random.randrange(1, precision, 1))
                for _ in range(count):
                    cards.append(half[side][0])
                    del half[side][0]
                loop_count += 1
                if loop_count > len(self.cards):
                    raise "Too many loops!"
            # Add any more remaining cards
            cards.extend(half[0])
            cards.extend(half[1])
            self.cards = cards
    '''
    Custom shuffle method where multiple players shuffle many decks together
    The method is to take a ~52 cards at a time shuffle once then trade half the cards for another set
    '''
    def multi_quick_shuffle(self, iterations = 1, precision = 10, players = None, num_players = None, seconds = 120) -> None:
        if players and num_players:
            raise "parameters players and num_players are mutually exclusive."
        if len(self.cards) < 52:
            raise "too few cards to shuffle"
        if not players:
            if not num_players: num_players = 4
            players = []
            for _ in range(num_players):
                players.append(Player(precision = precision))
        else:
            num_players = len(players)
        piles = self.split(num_players)
        for player in players:
            if hasattr(player, "multi_quick") and player.multi_quick:
                raise "Unexpected multi_quick_pile"
            player.multi_quick = SimpleNamespace()
            player.multi_quick.pile = None
        # iterate a second at a time
        while seconds > 0:
            for player in players:
                if player.multi_quick.pile == None or player.multi_quick.done_time >= seconds:
                    old_pile = None
                    if player.multi_quick.pile:
                        if player.multi_quick.pile.count() < 30:
                            old_pile = player.multi_quick.pile
                            player.multi_quick.pile = None
                        else:
                            old_pile = player.multi_quick.pile.split(2, include_current = True)[0]
                    if len(piles) > 0:
                        new_pile = random.choice(piles)
                        if player.multi_quick.pile:
                            max_count = 40
                        else:
                            max_count = 80
                        if new_pile.count() < max_count:
                            piles.remove(new_pile) # take whole pile
                        else:
                            new_pile = new_pile.split(2, include_current = True)[0]
                        if player.multi_quick.pile:
                            player.multi_quick.pile.add(new_pile)
                        else:
                            player.multi_quick.pile = new_pile
                        player.multi_quick.pile.shuffle(precision = player.precision, iterations = iterations, method = self.RIFFLE_SHUFFLE)
                        player.multi_quick.done_time = seconds - (max(1, int((5 + 10 * iterations) / player.speed))) \
                            - random.normalvariate(0, 3)
                    # now that we got a new file (or not) return the old one
                    if old_pile: piles.append(old_pile)
            seconds -= 1
        for player in players:
            piles.append(player.multi_quick.pile)
            player.multi_quick = None
        for pile in piles:
            self.add(pile)

    def __str__(self) -> str:
        s = "["
        if len(self.cards) == 0:
            s += "Empty"
        else:
            if self.face_up:
                s += str(self.peek())
            else:
                s += str(self.peek().back)
            s += "] ("+str(self.count())+")"
        return s
    def __repr__(self) -> str:
        return self.__str__()

class Hand(CardGroup):
    cards = None
    def __init__(self, cards = None):
        if cards == None: cards = list()
        self.cards = list(cards)
    def add(self, cards) -> None:
        self.cards.extend(cards)
    def remove(self, card) -> None:
        self.cards.remove(card)

    #def sort(self, method = SUITRANK):
    #    self.cards.sort()
    #def SUITRANK(card):
    #    return card.suit.value * 1 + card.rank.value * 1000
    def __str__(self) -> str:
        s = ""
        if len(self.cards) == 0:
            s += "[Empty"
        else:
            for card in self.cards:
                #if self.face_up:
                s += "["+card.get_shorthand()
                #else:
                #    s += "["+str(card.back)+"]"
        s += "]"
        return s

"""
A group of cards layed out so all can see them.
Similar to a Hand but typically not private.
"""
class Fan(CardGroup):
    cards = None
    def __init__(self, cards = None, face_up = True):
        if cards == None: cards = list()
        self.cards = list(cards)
        self.face_up = face_up
    def add(self, cards) -> None:
        self.cards.extend(cards)
    def remove(self, card) -> None:
        self.cards.remove(card)
    def __str__(self) -> str:
        s = ""
        if len(self.cards) == 0:
            s += "[Empty"
        else:
            for card in self.cards:
                #if self.face_up:
                s += "["+card.get_shorthand()
                #else:
                #    s += "["+str(card.back)+"]"
        s += "]"
        return s

class PlayingArea():
    groups = None
    def __init__(self, name = None, groups = None):
        self.name = name
        if groups == None: groups = list()
        self.groups = groups
    def combine_groups(self):
        pile = Pile()
        for group in self.groups:
            pile.add(group)
        self.groups = [pile]
    def clear_groups(self):
        pile = Pile()
        for group in self.groups:
            pile.add(group)
        self.groups = []
        return pile
    def append(self, group):
        if group in self.groups:
            raise "Group already in playing area!"
        self.groups.append(group)
    def transfer_cards(self, areas):
        for area in areas:
            self.groups.extend(area.groups)
            area.groups = []
    def includes_meld_type(self, meld_type, method):
        for group in self.groups:
            if group.includes_meld_type(meld_type = meld_type, method = method):
                return True
        return False
    def display(self):
        if self.name: print(self.name+":", end=" ")
        print("  ".join([str(x) for x in self.groups]))
#        Columns:
#        table_data = [
#            ['a', 'b', 'c'],
#            ['aaaaaaaaaa', 'b', 'c'],
#            ['a', 'bbbbbbbbbb', 'c']
#        ]
#        for row in table_data:
#            print("{: >20} {: >20} {: >20}".format(*row))


class Table():
    areas = players = None
    def __init__(self):
        self.areas = list()
        self.players = list()
    def add_area(self, area):
        if area in self.areas:
            raise "Area already on the table!"
        self.areas.append(area)
    def get_area(self, name):
        for area in self.areas:
            if area.name == name:
                return area
        raise "Area not found: "+name
    def add_player(self, player):
        if player in self.players:
            raise "Player already at the table: "+str(player)
        self.players.append(player)
    def display(self):
        for area in self.areas:
            area.display()
        for player in self.players:
            player.display()

class Player():
    name = areas = precision = speed = None
    def __init__(self, name = None, precision = 7, speed = 1.0):
        self.name = name
        self.precision = precision
        self.speed = speed
        self.areas = []
    def add_area(self, area):
        if area in self.areas:
            raise "Area already associated with Player!"
        self.areas.append(area)
    def get_area(self, name):
        for area in self.areas:
            if area.name == name:
                return area
        raise "Player area not found: "+name
    def get_hand(self):
        hand_area = self.get_area("hand")
        if len(hand_area.groups) != 1:
            raise ValueError("Expected one hand")
        return hand_area.groups[0]
    def display(self):
            print(self.name+":")
            self.display_areas()
    def display_areas(self):
        for area in self.areas:
            area.display()

'''
#print(len(Deck("Green").cards))
#print(Suit.CLUBS.value)
#p = Pile(Deck("Green").cards)
#print(p)
#p.flip()
#print(p)
p = Deck().get_pile()
#print(p.cards)
print(p.calc_entropy(method=Meld.RANKCOLOR))
p.shuffle(iterations=7, precision=10)
print(p.calc_entropy(method=Meld.RANKCOLOR))
#print(p.cards)
#print(p)
#print(Rank.parse("3"))
#print(Card.parse("AH"))
ps = p.deal(2, 3, face_up=True)
print(ps)
print(ps[0].count_melds(method=Meld.RANKCOLOR))
print(ps[1].count_melds(method=Meld.RANKCOLOR))
print(ps[0].calc_entropy(method=Meld.RANKCOLOR))
print(ps[1].calc_entropy(method=Meld.RANKCOLOR))
#'''
'''
table = Table()
area = PlayingArea("Main")
area.append(Deck().get_pile())
area.append(Deck().get_pile())
#area.display()
table.add_area(area)
table.display()
#'''

'''
p = Deck().get_pile()
p.add(Deck().get_pile())
p.add(Deck().get_pile())
p.add(Deck().get_pile())
p.add(Deck().get_pile())
p.sort(method = Meld.RANKCOLOR)
#print(p.calc_entropy(method=Meld.RANKCOLOR))
p.multi_quick_shuffle(seconds = 60 * 2, iterations = 1)
#print(p.cards)
p2 = p.deal(num_piles=1, num_cards=54)[0]
print(p2.calc_entropy(method=Meld.RANKCOLOR))
p.sort(method = Meld.RANKCOLOR)
p3 = p.deal(num_piles=1, num_cards=54)[0]
print(p3.calc_entropy(method=Meld.RANKCOLOR))
'''

p = Deck().get_pile()
p.draw(11)
p.draw(11)
print(p)
