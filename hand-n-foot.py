"""
  Simulate Hand and Foot card game
"""
import cards

class Strategy():
    laydown_dirty = True
    dirty_for_safety = True
    safe_when_missing_pile = True
    safe_when_hand_gt = 5
    prefer_high = True

def HNFGame():
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
        self.player.add_area(cards.PlayingArea(name="down"))
        self.player.add_area(cards.PlayingArea(name="hand"))
        self.table.add_player(player)
    def setup(self):
        if self.setup:
            return
        self.setup = True
        self.table.add_area(cards.PlayingArea(name="discard"))
        self.table.add_area(cards.PlayingArea(name="draw"))
        for _ in range(len(self.players) + 1):
            deck = cards.Deck()
            #self.decks.append(deck)
            self.table.get_area("discard").append(deck.get_pile())
        
    def start(self):
        self.setup()


    
