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

class HNFRules():
    def __init__(self):
        pass
    @classmethod
    def round_starting_points(cls, round):
        return [50, 75, 100, 150][round - 1]

class HNFGame():
    def __init__(self):
        self.setup = False
        self.players = []
        self.round = 0
        #self.decks = []
        #self.piles = []
        #self.table = cards.Table()
        self.table = cards.Table()
    def add_player(self, player, strategy):
        player.strategy = strategy
        self.players.append(player)
        player.add_area(cards.PlayingArea(name="complete"))
        player.add_area(cards.PlayingArea(name="down"))
        player.add_area(cards.PlayingArea(name="hand"))
        player.add_area(cards.PlayingArea(name="foot"))
        self.table.add_player(player)
    def get_card_points(self, card):
        if card.rank == cards.Rank.THREE and card.get_color == cards.Color.RED:
            return -300
        if card.rank == cards.Rank.JOKER:
            return 50
        if card.rank == cards.Rank.ACE or card.rank == cards.Rank.TWO:
            return 20
        if card.is_face_card():
            return 10
        else:
            return 5
    def get_points(self, group):
        if isinstance(group, cards.CardGroup):
            c = group.cards
        elif isinstance(group, 'list'):
            c = group
        else:
            raise TypeError("Unexpected get_points type: "+type(group))
        points = 0
        for card in c:
            points += self.get_card_points(card)
        return points
    def get_player_score(self, player):
        score = 0
        for group in player.get_area("complete").groups:
            score += self.get_points(group)
            if group.hnf_pure == True:
                score += 300
            else:
                score += 100
        for group in player.get_area("down").groups:
            score += self.get_points(group)
        for group in player.get_area("hand").groups:
            score -= self.get_points(group)
        for group in player.get_area("foot").groups:
            score -= self.get_points(group)
        return score

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
    def round_setup(self):
        self.round += 1
        if self.round > 4:
            raise ValueError("Too many rounds")
        discard_area = self.table.get_area("discard")
        draw_area = self.table.get_area("draw")
        #discard_area.display()
        #draw_area.display()
        # Move all cards into discard area
        for player in self.players:
            discard_area.transfer_cards(player.areas)
        discard_area.transfer_cards([draw_area])
        # Shuffle all cards together
        pile = discard_area.clear_groups()
        pile.multi_quick_shuffle(players = self.players)
        for draw_pile in pile.split(num_piles=len(self.players)):
            draw_area.append(draw_pile)
        #draw_area.display()
        for idx, player in enumerate(self.players):
            # Get hands from decks in front of other players
            hands = list()
            hands.append(cards.Pile(cards = draw_area.groups[(idx - 1) % len(self.players)].draw(number = 11)))
            hands.append(cards.Pile(cards = draw_area.groups[(idx + 1) % len(self.players)].draw(number = 11)))
            #draw_area.display()
            player.get_area("foot").append(hands.pop(random.randrange(len(hands))))
            player.get_area("foot").groups[0].sort(method = cards.CardGroup.RANKCOLOR)
            player.get_area("hand").append(cards.Hand(hands.pop().cards))
            player.get_area("hand").groups[0].sort(method = cards.CardGroup.RANKCOLOR)
    def display(self):
        for player in self.players:
            print(player.name+": "+str(self.get_player_score(player)))
        print("")
        self.table.display()
    def play_turn(self, player):
        # draw
        # add to down area melds and complete piles
        # add new melds
        # take foot and repeat
        # make piles
        # discard
        pass # TODO
    def draw(self, player):
        # select pile
        pile_idx = self.players.index(player)
        draw_area = self.table.get_area("draw")
        cards = []
        while(len(cards) < 2):
            draw_pile = draw_area.groups[(pile_idx ) % len(draw_area.groups)]
            cards.extend(draw_pile.draw(number = 2 - len(cards)))
            pile_idx += 1
            if pile_idx > len(draw_area.groups):
                raise(ValueError("Can't find card"))
        player.get_area("hand").groups[0].add(cards)
    def get_ready_melds(self, player):
        melds = player.get_area("hand").groups[0].get_melds(cards.CardGroup.RANKCOLOR)
        ready = []
        for meld in melds:
            if len(meld) >= 3:
                ready.append(meld)
        return ready
    def can_lay_down(self, player):
        melds = self.get_ready_melds(player)
        points = 0
        for meld in melds:
            points += self.get_points(meld)
        if points > HNFRules.round_starting_points(self.round):
            return True
        return False
    def start(self):
        self.game_setup()
        self.round_setup()

g = HNFGame()
g.add_player(cards.Player("J", precision=5, speed=1.2), Strategy())
g.add_player(cards.Player("S", precision=10, speed=1), Strategy())
g.add_player(cards.Player("L", precision=7, speed=1), Strategy())
g.add_player(cards.Player("A", precision=15, speed=.9), Strategy())
#g.game_setup()
#g.round_setup()
g.start()
#g.display()

g.players[0].display()
g.draw(player = g.players[0])
g.players[0].display()
