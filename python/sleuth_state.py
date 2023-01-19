import itertools as it

import re

direct_card_input = re.compile("(.*)\[(.*)\]")

ColorPossibilities = set(['R', 'B', 'Y', 'G'])
NumberPossibilities = set(['1', '2', '3'])
StonePossibilities = set(['D', 'O', 'P'])
FullDeck = [i for i in it.product(ColorPossibilities, NumberPossibilities, StonePossibilities)]
class Knowledge(object):
    def __init__(self, knowledge):
        player_num, num, question_asked, cards = knowledge
        self.player_num = player_num
        self.num = num
        self.question_asked = question_asked
        self.cards = cards

class Player(object):
    def __init__(self):
        self.cards = []
    
    def set_cards(self, cards):
        self.cards = set(cards)

class Opponent(object):
    def __init__(self, hand_size):
        self.hand_size = hand_size
        self.cardPotentials = []
        self.knowledge = []

    def init_opponent(self, remaining_deck):
        self.cardPotentials = [set(i) for i in it.combinations(remaining_deck, self.hand_size)]

    def add_knowledge(self, knowledge: Knowledge):
        # Check the number of cards/attributes and remove invalid states for a given hand
        # check all states for cards that are in all of them, add to known cards list so we can eliminate states from other players
        self.cardPotentials = [i for i in self.cardPotentials]
        
def parse_new_knowledge(knowledge: str): #1:1,BD[R1P]
    player_num, real_knowledge = knowledge.split(":")
    print(real_knowledge)
    num, b = real_knowledge.split(",")
    has_specific_cards = direct_card_input.match(b)
    card_tups = None
    question_asked = None
    if has_specific_cards:
        card_tups = [str_to_card_tup(_str) for _str in has_specific_cards.group(2).split(";")]
        question_asked = has_specific_cards.group(1)
    else:
        question_asked = b
    return Knowledge((int(player_num), int(num), question_asked, card_tups))

class GameState(object):
    def __init__(self, player_count):
        self.hand_size = (36 - 1)/player_count 
        print(hand_size)
        self.player = Player()
        self.opponents = [Opponent(self.hand_size) for i in range(player_count-1)]
        self.game_state = set(FullDeck)
        self.knowledge = []


    def init_public_knowledge(self, faceup_cards):
        self.faceup_cards = set(faceup_cards)
        self.game_state -= self.faceup_cards
    
    def init_player(self, player_cards):
        self.player.set_cards(player_cards)
        self.game_state -= self.player.cards
    
    def ready(self):
        for opponent in self.opponents:
            opponent.init_opponent(self.game_state)

    def add_knowledge(self, knowledge_string):
        knowledge = parse_new_knowledge(knowledge_string)
        self.knowledge.append(knowledge)
        self.opponents[knowledge.player_num-1].add_knowledge(knowledge)


bool_conv = {"false": False, "true": True}
def str_to_card_tup(str_val):
    return (str_val[0], str_val[1], str_val[2])

with open("INPUT.txt") as f:
    f_lines = [line for line in f]
player_cards = [str_to_card_tup(i.strip()) for i in f_lines[0].split(",")]
face_up = [str_to_card_tup(i.strip()) for i in f_lines[1].split(",")]
hand_size = int(f_lines[2])
game = GameState(4)
game.init_public_knowledge(face_up)
game.init_player(player_cards)
game.ready()
knowledge_lines = f_lines[4:]
for line in knowledge_lines:
    game.add_knowledge(line)