"""
  Simulate Hand and Foot card game
"""
import random
import logging
from types import SimpleNamespace
import cardtable

class Strategy(SimpleNamespace):
    DRAW_CLOSEST = 1
    DRAW_RANDOM = 2
    DRAW_HAND_SOURCE = 3
    DRAW_FOOT_SOURCE = 4
    DRAW_CURRENT_SOURCE = 5
    def __init__(self):
        laydown_dirty = True
        dirty_for_safety = True
        safe_when_missing_pile = True
        safe_when_hand_gt = 5
        prefer_high = True
        draw_from = self.DRAW_CLOSEST

class HNFRules():
    DIRTY_MAX_MINORITY = 1 # Wilds need to be minority of cards in fan
    def __init__(self):
        allow_discard_to_end_last_round = False
        allow_melds_of_threes = False
        allow_melds_of_wilds = False
        allow_add_wilds_to_existing_piles = False
        dirty_wildcard_max_rule = self.DIRTY_MAX_MINORITY
        pass
    @classmethod
    def round_starting_points(cls, round):
        return [50, 75, 100, 150][round - 1]

class HNFGame():
    def __init__(self):
        self.setup = False
        self.players = []
        self.round = 0
        #self.packs = []
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
        logging.info("Setting up game")
        self.setup = True
        self.table.add_area(cardtable.PlayingArea(name="discard"))
        self.table.add_area(cardtable.PlayingArea(name="draw"))
        for _ in range(len(self.players) + 1):
            pack = cardtable.Pack()
            #self.packs.append(pack)
            self.table.get_area("discard").append(pack.get_pile())
    def round_setup(self):
        self.round += 1
        logging.info("Setting up round "+str(self.round))
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
            # Get hands from packs in front of other players
            hands = list()
            hands.append(cardtable.Pile(cards = draw_area.groups[(idx - 1) % len(self.players)].draw(number = 11)))
            hands.append(cardtable.Pile(cards = draw_area.groups[(idx + 1) % len(self.players)].draw(number = 11)))
            #draw_area.display()
            player.get_area("foot").append(hands.pop(random.randrange(len(hands))))
            player.get_area("foot").groups[0].sort(method = cardtable.Meld.RANKCOLOR)
            player.get_area("hand").append(cardtable.Hand(hands.pop().cards))
            player.get_area("hand").groups[0].sort(method = cardtable.Meld.RANKCOLOR)
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
        if not player.hnf_is_down:
            if self.can_lay_down(player):
                melds = self.get_ready_melds(player)
                for meld in melds:
                    self.lay_down(player, cards = list(meld))
        else:
            melds = player.get_hand().get_melds(cardtable.Meld.RANKCOLOR)
            for meld in melds:
                if len(meld)>=3 or player.get_area("down").includes_meld_type(meld.get_type()):
                    self.lay_down(player, cards = list(meld))
            #TODO play wild cards?
            # TODO for each meld > 3 and if down area.includes_meld then play
            pass #TODO
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
        logging.debug(f"Player {player.name} draws {cardtable.cards_to_str(cards)}")
        player.get_hand().add(cards)
        player.get_hand().sort(method = cardtable.Meld.RANKCOLOR)
    def lay_down(self, player, cards):
        logging.debug(f"Player {player.name} lays down {cardtable.cards_to_str(cards)}")
        hand = player.get_hand()
        down_area = player.get_area(name = "down")
        piles_area = player.get_area(name = "complete")
        for card in cards:
            hand.remove(card)
        down_area.add_to_group_by_meld_type(cards = cards, method = cardtable.Meld.RANKCOLOR, group_cls = cardtable.Fan)
        #TODO add fans to piles
        #TODO check that fans have at least 3.
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
        melds = hand.get_melds(method = cardtable.Meld.RANKCOLOR)
        melds.sort(key=len)
        card = melds[0][0]
        hand.remove(card)
        self.table.get_area("discard").groups[0].push(card)
        """
        Get cards sorted by desirability (from strategy)
        """

        pass #TODO
    def get_ready_melds(self, player):
        melds = player.get_hand().get_melds(cardtable.Meld.RANKCOLOR)
        # TODO need to take into account wilds. They can't form meld
        ready = []
        for meld in melds:
            if len(meld) >= 3:
                ready.append(meld)
        return ready
    def can_lay_down(self, player):
        melds = self.get_ready_melds(player)
        # TODO need to take into account wilds
        points = 0
        for meld in melds:
            points += self.get_points(meld)
        if points > HNFRules.round_starting_points(self.round):
            return True
        return False
    def start(self):
        self.game_setup()
        self.round_setup()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
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
    for i in range(20):
        g.play_turn(player = g.players[0])
    g.players[0].display()
