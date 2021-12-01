"""
  Simulate Hand and Foot card game
"""
import cards
from types import SimpleNamespace
import random

class Strategy(SimpleNamespace):
    laydown_dirty = True
    dirty_for_safety = True
    safe_when_missing_pile = True
    safe_when_hand_gt = 5
    prefer_high = True
    draw_from = 'closest' # random, hand source, foot source

class HNFGame():
    def __init__(self):
        self.setup = False
        self.players = []
        #self.decks = []
        #self.piles = []
        #self.table = cards.Table()
        self.table = cards.Table()
    def add_player(self, player, strategy):
        player.strategy = strategy
        self.players.append(player)
        player.add_area(cards.PlayingArea(name="down"))
        player.add_area(cards.PlayingArea(name="hand"))
        player.add_area(cards.PlayingArea(name="foot"))
        self.table.add_player(player)
    def game_setup(self):
        if self.setup:
            return
        print("Setting up game")
        self.setup = True
        self.table.add_area(cards.PlayingArea(name="discard"))
        self.table.add_area(cards.PlayingArea(name="draw"))
        for _ in range(len(self.players) + 1):
            deck = cards.Deck()
            #self.decks.append(deck)
            self.table.get_area("discard").append(deck.get_pile())
    def hand_setup(self):
        discard_area = self.table.get_area("discard")
        # Move all cards into discard area
        for player in self.players:
            discard_area.transfer_cards(player.areas)
        discard_area.transfer_cards([self.table.get_area("draw")])
        # Shuffle all cards together
        pile = discard_area.clear_groups()
        pile.multi_quick_shuffle(players = self.players)
        draw_area = self.table.get_area("draw")
        for draw_pile in pile.split(num_piles=len(self.players)):
            draw_area.append(draw_pile)
        for idx, player in enumerate(self.players):
            # Get hands from decks in front of other players
            hands = []
            hands.append(cards.Pile(cards = draw_area.groups[(idx - 1) % len(self.players)].draw(11)))
            hands.append(cards.Pile(cards = draw_area.groups[(idx + 1) % len(self.players)].draw(11)))
            player.get_area("foot").append(random.choice(hands))
            player.get_area("hand").append(cards.Hand(random.choice(hands).cards))


        
    def start(self):
        self.game_setup()
        self.hand_setup()

g = HNFGame()
g.add_player(cards.Player("J", precision=5, speed=1.2), Strategy())
g.add_player(cards.Player("S", precision=10, speed=1), Strategy())
g.add_player(cards.Player("L", precision=7, speed=1), Strategy())
g.add_player(cards.Player("A", precision=15, speed=.9), Strategy())
g.start()
g.table.display()


    
