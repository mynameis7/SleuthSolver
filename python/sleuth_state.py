import itertools as it



class CardSuperPosition(object):
    def __init__(self):
        self.possibilities = set(deck)

    
class Player(object):
    def __init__(self):
        self.cards = []
    
    def set_cards(self, cards):
        self.cards = cards

class Opponent(object):
    def __init__(self, numCards):
        self.cardPotentials = [CardSuperPosition() for i in range(numCards)]
    
    def process_card_potentials(self, game_state, knowledge):


class GameState(object):
    def __init__(self):
        self.player = Player()
        self.opponents = [Opponent(8), Opponent(8), Opponent(8)]
        self.game_state = set(it.product(ColorPossibilities, NumberPossibilities, StonePossibilities))
    
    def init_player(self, player_cards):
        self.player.set_cards(player_cards)
        set(player_cards)