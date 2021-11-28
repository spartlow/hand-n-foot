"""
Classes for a standard deck of cards
"""
import itertools
from enum import Enum
import random
import math

BACKS = ["B", "R", "G", "Y", "K"]
def get_next_back():
    get_next_back.back_idx += 1
    return (BACKS[get_next_back.back_idx % 2] + str(get_next_back.back_idx // 2 + 1))
get_next_back.back_idx = -1

class Color(Enum):
    RED = 1
    BLACK = 2
    def __repr__(self):
        return self.name+"!"
    def __str__(self):
        return self.name

from enum import Enum
class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4
    BLACK = 5 # For Jokers
    RED = 6 # For Jokers
    def _get_shorthands(self):
        return ["H", "D", "S", "C", "B", "R"]
    def get_shorthand(self):
        return self._get_shorthands()[self.value - 1]
    def get_color(self):
        return [Color.RED, Color.RED, Color.BLACK, Color.BLACK, Color.BLACK, Color.RED][self.value - 1]
    def __repr__(self):
        return self.name+"!"
    def __str__(self):
        return self.name
    @classmethod
    def _shorthands(self):
        return ["H", "D", "S", "C", "B", "R"]
    @classmethod
    def parse(cls, shorthand):
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
    def _get_shorthands(self):
        return ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "*"]
    def get_shorthand(self):
        return self._get_shorthands()[self.value - 1]
    def is_face_card(self):
        if self.rank.value >= self.JACK and self.rank.value <= self.KING: # Jokers are not considered face cards
            return True
        else:
            return False 
    def __repr__(self):
        return self.name+"!"
    def __str__(self):
        return self.name
    @classmethod
    def _shorthands(self):
        return ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "*"]
    @classmethod
    def parse(cls, shorthand):
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
    def __repr__(self):
        return str(self.back)+" "+str(self.rank)+" of "+str(self.suit)# +" is "+str(self.suit.get_color())
    def get_shorthand(self):
        return self.rank.get_shorthand()+self.suit.get_shorthand()
    def is_face_card(self):
        return self.rank.is_face_card()
    def get_color(self):
        return self.suit.get_color()
    def count_eyes(self):
        if self.rank == Rank.JOKER:
            return 2
        elif self.is_face_card():
            if self.get_shorthand in ["JS", "JH", "KD"]:
                return 1
            return 2
        elif self.rank == Rank.JOKER:
            return 2
        return 0
    def get_unicode(self):
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
    @classmethod
    def parse(cls, shorthand, back = ""):
        return cls(Rank.parse(shorthand[0]), Suit.parse(shorthand[1]), back)

"""
Defines a deck of cards
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
    def get_pile(self, face_up = False):
        return Pile(self.cards)

class CardGroup():
    cards = None
    RANKCOLOR = 1
    def count(self):
        return len(self.cards)
    def __str__(self):
        return str(self)
    def count_sets(self, method):
        if method == self.RANKCOLOR:
            sets = set()
            for card in self.cards:
                sets.add(card.rank.get_shorthand()+str(card.get_color()))
            print(sets)
            return len(sets)
        else:
            raise "Unknown count_sets method: "+str(method)
    def calc_entropy(self, method):
        # See https://stackoverflow.com/questions/19434884/determining-how-well-a-deck-is-shuffled
        if method == self.RANKCOLOR:
            num_sets = self.count_sets(method=method)
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
    def __init__(self, cards = None, face_up = False):
        if cards == None: cards = list()
        self.cards = cards
        self.face_up = face_up
    def pop(self):
        return self.cards.pop()
    def draw(self, number = 1):
        cards = []
        for i in range(number):
            cards.append(self.pop())
        return cards
    def peek(self):
        return self.cards[-1]
    def push(self, card):
        self.cards.append(card)
    def add(self, cards):
        self.cards.extend(cards)
    def flip(self):
        self.face_up = not self.face_up
        self.cards.reverse()
    def deal(self, num_piles, num_cards = 1, face_up = False):
        piles = []
        for _ in range(num_piles):
            piles.append(Pile(face_up = face_up))
        for _ in range(num_cards):
            for p_idx in range(num_piles):
                card = self.pop()
                if card == None:
                    raise "No more cards to deal!"
                print(str(card)+" to pile "+str(p_idx))
                piles[p_idx].push(card)
        return piles

    def shuffle(self, iterations = 1, precision = 1):
        #random.shuffle(self.cards)
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

    def __str__(self):
        s = ""
        if len(self.cards) == 0:
            s += "Empty"
        else:
            if self.face_up:
                s += str(self.peek())
            else:
                s += str(self.peek().back)
            s += " ("+str(self.count())+")"
        return s
    def __repr__(self):
        return self.__str__()

class Hand(CardGroup):
    cards = None
    def __init__(self, cards = None):
        if cards == None: cards = list()
        self.cards = cards
    def add(self, cards):
        self.cards.extend(cards)
    def remove(self, card):
        self.remove(card)
    #def sort(self, method = SUITRANK):
    #    self.cards.sort()
    #def SUITRANK(card):
    #    return card.suit.value * 1 + card.rank.value * 1000

class PlayingArea():
    groups = None
    def __init__(self, name = None, groups = None):
        self.name = name
        if groups == None: groups = list()
        self.groups = groups
    def append(self, group):
        if group in self.groups:
            raise "Group already in playing area!"
        self.groups.append(group)
    def display(self):
        if self.name: print(self.name+":")
        print("  ".join([str(x) for x in self.groups]))
    def display_row(self, row_idx):
        pass    
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
    def add_player(self, player):
        if player in self.players:
            raise "Player already at the table: "+str(player)
        self.player.append(player)
    def display(self):
        for area in self.areas:
            area.display()
        for player in self.players:
            print(player.name+":")
            player.display_areas()

#print(len(Deck("Green").cards))
#print(Suit.CLUBS.value)
#p = Pile(Deck("Green").cards)
#print(p)
#p.flip()
#print(p)
p = Deck().get_pile()
#print(p.cards)
print(p.calc_entropy(method=CardGroup.RANKCOLOR))
p.shuffle(iterations=7, precision=10)
print(p.calc_entropy(method=CardGroup.RANKCOLOR))
#print(p.cards)
#print(p)
#print(Rank.parse("3"))
#print(Card.parse("AH"))
ps = p.deal(2, 3, face_up=True)
print(ps)
print(ps[0].count_sets(method=CardGroup.RANKCOLOR))
print(ps[1].count_sets(method=CardGroup.RANKCOLOR))
print(ps[0].calc_entropy(method=CardGroup.RANKCOLOR))
print(ps[1].calc_entropy(method=CardGroup.RANKCOLOR))

'''
table = Table()
area = PlayingArea("Main")
area.append(Deck().get_pile())
area.append(Deck().get_pile())
#area.display()
table.add_area(area)
table.display()
'''
