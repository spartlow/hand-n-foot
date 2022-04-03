"""
  Simulate Hand and Foot card game
"""
import cardtable
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
        self.table = cardtable.Table()
    def add_player(self, player, strategy):
        player.strategy = strategy
        self.players.append(player)
        player.add_area(cardtable.PlayingArea(name="complete"))
        player.add_area(cardtable.PlayingArea(name="down"))
        player.add_area(cardtable.PlayingArea(name="hand"))
        player.add_area(cardtable.PlayingArea(name="foot"))
        self.table.add_player(player)
    def get_card_points(self, card):
        if card.rank == cardtable.Rank.THREE and card.get_color == cardtable.Color.RED:
            return -300
        if card.rank == cardtable.Rank.JOKER:
            return 50
        if card.rank == cardtable.Rank.ACE or card.rank == cardtable.Rank.TWO:
            return 20
        if card.is_face_card() or card.rank == cardtable.Rank.TEN:
            return 10
        else:
            return 5
    def get_points(self, group):
        if isinstance(group, cardtable.CardGroup):
            c = group.cards
        elif isinstance(group, cardtable.Meld):
            c = list(group)
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
        self.table.add_area(cardtable.PlayingArea(name="discard"))
        self.table.add_area(cardtable.PlayingArea(name="draw"))
        for _ in range(len(self.players) + 1):
            deck = cardtable.Deck()
            #self.decks.append(deck)
            self.table.get_area("discard").append(deck.get_pile())
    def round_setup(self):
        self.round += 1
        if self.round > 4:
            raise ValueError("Too many rounds")
        for player in self.players:
            player.hnf_in_foot = False
            player.hnf_is_down = False
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
        discard_area.append(cardtable.Pile())
        pile.multi_quick_shuffle(players = self.players)
        for draw_pile in pile.split(num_piles=len(self.players)):
            draw_area.append(draw_pile)
        #draw_area.display()
        for idx, player in enumerate(self.players):
            # Get hands from decks in front of other players
            hands = list()
            hands.append(cardtable.Pile(cards = draw_area.groups[(idx - 1) % len(self.players)].draw(number = 11)))
            hands.append(cardtable.Pile(cards = draw_area.groups[(idx + 1) % len(self.players)].draw(number = 11)))
            #draw_area.display()
            player.get_area("foot").append(hands.pop(random.randrange(len(hands))))
            player.get_area("foot").groups[0].sort(method = cardtable.CardGroup.RANKCOLOR)
            player.get_area("hand").append(cardtable.Hand(hands.pop().cards))
            player.get_area("hand").groups[0].sort(method = cardtable.CardGroup.RANKCOLOR)
    def display(self):
        for player in self.players:
            print(player.name+": "+str(self.get_player_score(player)))
        print("")
        self.table.display()
    def play_turn(self, player):
        hand = player.get_hand()
        # draw
        self.draw(player)
        # add to down area melds and complete piles
        if player.hnf_is_down:
            # need area.includes_meld
            pass #TODO
        else:
            pass #TODO
        # add new melds
        # take foot and repeat
        # make piles
        # discard
        self.discard(player)
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
        player.get_hand().add(cards)
        player.get_hand().sort(method = cardtable.CardGroup.RANKCOLOR)
    def get_card_desirability(self, strategy, card, meld_size):
        """ Preference:
                If have incomplete pile
                Wild card (unless too many??)
                If have complete pile (7+) -- how to account for wildcards in piles or potential wildcards?
                If have ready meld (3-6)
                If have pair (2)
                If high card (or low if prefer low)
                #TODO move to strategy
        """
        '''
        if meld_size < 3:
            desirability = meld_size * 1000
            if strategy.prefer_high:
                desirability +=
        # '''
        pass #TODO
    def discard(self, player):
        # Temp simple code
        hand = player.get_hand()
        if len(hand.cards) == 0:
            raise ValueError("Can't discard from empty hand!")
        melds = hand.get_melds(method = cardtable.CardGroup.RANKCOLOR)
        melds.sort(key=len)
        card = melds[0][0]
        hand.remove(card)
        self.table.get_area("discard").groups[0].push(card)
        """
        Get cards sorted by desirability (from strategy)
        """

        pass #TODO
    def get_ready_melds(self, player):
        melds = player.get_hand().get_melds(cardtable.CardGroup.RANKCOLOR)
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
g.add_player(cardtable.Player("J", precision=5, speed=1.2), Strategy())
g.add_player(cardtable.Player("S", precision=10, speed=1), Strategy())
g.add_player(cardtable.Player("L", precision=7, speed=1), Strategy())
g.add_player(cardtable.Player("A", precision=15, speed=.9), Strategy())
#g.game_setup()
#g.round_setup()
g.start()
#g.display()

g.players[0].display()
g.play_turn(player = g.players[0])
g.players[0].display()
