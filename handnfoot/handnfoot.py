"""
  Simulate Hand and Foot card game
"""
import random
import logging
from types import SimpleNamespace
from . import cardtable

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
        self.allow_discard_to_end_last_round = False
        self.allow_melds_of_threes = True
        self.allow_melds_of_wilds = False
        self.allow_add_wilds_to_existing_piles = False
        self.dirty_wildcard_max_rule = self.DIRTY_MAX_MINORITY
        cardtable.Modifiers.set_wild_ranks([cardtable.Rank.TWO, cardtable.Rank.JOKER])
        cardtable.Modifiers.set_meld_method(cardtable.Meld.RANK)
        self.rank_points = { \
            cardtable.Rank.TWO:   20, \
            cardtable.Rank.THREE:  5, \
            cardtable.Rank.FOUR:   5, \
            cardtable.Rank.FIVE:   5, \
            cardtable.Rank.SIX:    5, \
            cardtable.Rank.SEVEN:  5, \
            cardtable.Rank.EIGHT:  5, \
            cardtable.Rank.NINE:   5, \
            cardtable.Rank.TEN:   10, \
            cardtable.Rank.JACK:  10, \
            cardtable.Rank.QUEEN: 10, \
            cardtable.Rank.KING:  10, \
            cardtable.Rank.ACE:   20, \
            cardtable.Rank.JOKER: 50}
    def get_card_points(self, card):
        if card.get_shorthand() in ["3D", "3H"]:
            return -300
        else:
            return self.rank_points[card.rank]
    @classmethod
    def round_starting_points(cls, round):
        return [50, 75, 100, 150][round - 1]

class HNFGame():
    def __init__(self):
        self.setup = False
        self.players = []
        self.round = 0
        self.round_complete = False
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
            player.get_area("foot").groups[0].sort(method = cardtable.Meld.RANK)
            player.get_area("hand").append(cardtable.Hand(hands.pop().cards))
            player.get_area("hand").groups[0].sort(method = cardtable.Meld.RANK)
    def display(self):
        for player in self.players:
            print(player.name+": "+str(self.get_player_score(player)))
        print("")
        self.table.display()
    def play_turn(self, player):
        if self.round_complete:
            raise ValueError("Round is over!")
        method = cardtable.Meld.RANK
        hand = player.get_hand()
        foot = player.get_foot()
        # draw
        self.draw(player)
        # add to down area melds and complete piles
        keep_playing = True
        while keep_playing:
            if not player.hnf_is_down:
                # TODO combine with below?
                if self.can_lay_down(player):
                    melds = self.get_ready_melds(player)
                    for meld in melds:
                        self.lay_down_meld(player, meld = meld)
            else:
                melds = hand.get_melds(method = cardtable.Meld.RANK, exclude_wilds = True)
                singleton_cnt = 0
                pair_cnt = 0
                for meld in melds:
                    #print(str(len(meld))+" "+meld.get_type())
                    if len(meld)>=3 or player.get_area("down").includes_meld_type(meld.get_type(), method = method) \
                            or player.get_area("complete").includes_meld_type(meld.get_type(), method = method):
                        self.lay_down_meld(player, meld = meld)
                    else:
                        if len(meld) == 1:
                            singleton_cnt += 1
                        elif len(meld) == 2:
                            pair_cnt += 1
                        else:
                            raise ValueError("Unexpected leftover meld length of "+len(meld))
                    #    print(player.get_area("down").includes_meld_type(meld.get_type(), method = method))
                #TODO play wild cards?
                wilds = hand.get_wilds()
                if len(wilds) > 0:
                    if len(wilds) == pair_cnt and singleton_cnt == 0:
                        melds = hand.get_melds(cardtable.Meld.RANK, exclude_wilds = True)
                        for meld in melds:
                            if len(meld) != 2:
                                raise ValueError("Unexpected pair meld length of "+len(meld))
                            meld.append(wilds.pop()) # TODO use highest value wild
                            self.lay_down_meld(player, meld = meld)
                    elif pair_cnt == 0 and singleton_cnt == 0:
                        # dirty some piles
                        down_groups = player.get_area(name = "down").get_groups()
                        down_groups.sort(key=len)
                        for group in down_groups:
                            meld_type = group.cards[0].get_meld_type()
                            # TODO need to check if can handle that many wilds
                            # TODO add wilds to dirty fans first
                            self.lay_down_cards_by_meld(player, wilds.pop(), meld_type = meld_type)
                            if len(wilds) == 0:
                                break

                # TODO for each meld > 3 and if down area.includes_meld then play
                pass #TODO
            # make piles?
            # Discard
            if len(hand) > 0:
                self.discard(player)
                keep_playing = False
            if len(hand) == 0:
                if len(foot) == 0:
                    logging.debug(f"Player {player.name} ends the round!")
                    keep_playing = False
                    self.round_complete = True
                else:
                    if keep_playing:
                        logging.debug(f"Player {player.name} picks up their foot and keeps playing!")
                    else:
                        logging.debug(f"Player {player.name} picks up their foot.")
                    hand.add(foot.remove_all_cards())
                    player.hnf_in_foot = True
    def draw(self, player):
        # select pile
        pile_idx = self.players.index(player)
        draw_area = self.table.get_area("draw")
        cards = []
        while(len(cards) < 2):
            draw_pile = draw_area.groups[(pile_idx ) % len(draw_area.groups)]
            if len(draw_pile.cards) > 0:
                cards.extend(draw_pile.draw(number = 2 - len(cards)))
            pile_idx += 1
            if pile_idx > len(draw_area.groups):
                raise(ValueError("Can't find card"))
        logging.debug(f"Player {player.name} draws {cardtable.cards_to_str(cards)}")
        player.get_hand().add(cards)
        player.get_hand().sort(method = cardtable.Meld.RANK)
    def lay_down_meld(self, player, meld):
        cards = list(meld)
        meld_type = meld.get_type()
        if meld_type == "WILD":
            raise ValueError("Trying to lay down wild meld")
        logging.debug(f"Player {player.name} lays down {cardtable.cards_to_str(cards)} of type {cards[0].get_meld_type(method=cardtable.Meld.RANK)}")
        hand = player.get_hand()
        down_area = player.get_area(name = "down")
        hand.remove_cards(cards)
        down_area.add_to_group_by_meld_type(cards = cards, group_cls = cardtable.Fan, meld_type = meld_type, method = cardtable.Meld.RANK)
        self.add_fans_to_piles(player = player)
        #TODO check that fans have at least 3.
        player.hnf_is_down = True
    def lay_down_card_by_meld(self, player, card, meld_type):
        cards = [card]
        logging.debug(f"Player {player.name} lays down card {cardtable.cards_to_str(cards)}")
        hand = player.get_hand()
        down_area = player.get_area(name = "down")
        hand.remove_cards(cards)
        down_area.add_to_group_by_meld_type(cards = cards, group_cls = cardtable.Fan, meld_type = meld_type, method = cardtable.Meld.RANK)
        self.add_fans_to_piles(player = player)
        #TODO check that fans have at least 3.
        player.hnf_is_down = True
    def add_fans_to_piles(self, player):
        method = cardtable.Meld.RANK
        down_area = player.get_area(name = "down")
        complete_area = player.get_area(name = "complete")
        for fan in down_area.groups:
            if len(fan.cards) == 0:
                continue # or remove it?
            meld_type = fan.cards[0].get_meld_type(method = method)
            pile = complete_area.get_group_by_meld_type(meld_type = meld_type, method = method)
            if pile is None and len(fan.cards) >= 7:
                pile = cardtable.Pile()
                pile.face_up = True
                pile.hnf_clean = True # TODO if has wildcards mark dirty
                complete_area.append(pile)
            if pile is not None:
                logging.debug(f"Player {player.name} added {cardtable.cards_to_str(fan.cards)} to a pile")
                pile.add(fan.cards)
                fan.cards = []
                #player.display()
        down_area.remove_empty_groups()
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
        melds = hand.get_melds(method = cardtable.Meld.RANK)
        melds.sort(key=len)
        card = melds[0][0]
        hand.remove(card)
        logging.debug(f"Player {player.name} discards {card.get_shorthand()} leaving {cardtable.cards_to_str(hand.cards)}")
        self.table.get_area("discard").groups[0].push(card)
        """
        Get cards sorted by desirability (from strategy)
        """

        pass #TODO
    def get_ready_melds(self, player):
        melds = player.get_hand().get_melds(cardtable.Meld.RANK, exclude_wilds = True)
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
    for i in range(50):
        g.play_turn(player = g.players[0])
    g.players[0].display()
