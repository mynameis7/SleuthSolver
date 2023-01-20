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
    def __str__(self):
        return f"{self.question_asked}? => {self.num}{(','+self.cards) if self.cards else ''}"

class Player(object):
    def __init__(self):
        self.cards = []
    
    def set_cards(self, cards):
        self.cards = set(cards)

class Opponent(object):
    def __init__(self, hand_size):
        self.hand_size = hand_size
        self.card_potentials = []
        self.knowledge = []

    def init_opponent(self, remaining_deck):
        self.card_potentials = [set(i) for i in it.combinations(remaining_deck, self.hand_size)]

    def add_knowledge(self, knowledge: Knowledge):
        self.knowledge.append(knowledge)
        # Check the number of cards/attributes and remove invalid states for a given hand
        # check all states for cards that are in all of them, add to known cards list so we can eliminate states from other players
        self.card_potentials = [i for i in self.card_potentials if self.passes(i)]
        return self.find_certain_cards()

    def find_certain_cards(self):
        pass
    
    def passes(self, hand):
        def explicit_card_missing(e:Knowledge, player):
            if e.cards:
                for card in e.cards:
                    if card not in player:
                        return True
            return False
        def filter_attribute(cards, attribute):
            if not attribute:
                return cards
            return [i for i in cards if attribute in i]
        def question_asked_fail(e:Knowledge, player):
            color = list(ColorPossibilities.intersection(e.question_asked))
            number = list(NumberPossibilities.intersection(e.question_asked))
            stone = list(StonePossibilities.intersection(e.question_asked))
            color = color[0] if color else None
            number = number[0] if number else None
            stone = stone[0] if stone else None
            if element.num > 0:
                final = filter_attribute(player, color)
                final = filter_attribute(final, number)
                final = filter_attribute(final, stone)
                if len(final) != element.num:
                    return True
            return False
        def has_invalid_non_cards(e:Knowledge, player):
            if e.num == 0:
                color = list(ColorPossibilities.intersection(e.question_asked))
                number = list(NumberPossibilities.intersection(e.question_asked))
                stone = list(StonePossibilities.intersection(e.question_asked))
                color = color[0] if color else None
                number = number[0] if number else None
                stone = stone[0] if stone else None
                if color and len([i for i in player if color in i]) > 0:
                    return True
                if number and len([i for i in player if number in i]) > 0:
                    return True
                if stone and len([i for i in player if stone in i]) > 0:
                    return True
                return False

        for element in self.knowledge:
            player = set(hand)
            if explicit_card_missing(element, player):
                return False
            if has_invalid_non_cards(element, player):
                return False
            if question_asked_fail(element, player):
                return False
        return True

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
        self.hand_size = int((36 - 1)/player_count)
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
        new_solved_cards = self.opponents[knowledge.player_num-1].add_knowledge(knowledge)


bool_conv = {"false": False, "true": True}
def str_to_card_tup(str_val):
    return (str_val[0], str_val[1], str_val[2])

with open("INPUT.txt") as f:
    f_lines = [line.strip() for line in f]
# f_lines = [
#     "R1D, B3P, R2O, Y3P, G1D, Y1O, B2D,G3D",
#     "B2P, Y1P, G2P",
#     "8",
#     "False",
#     "1:0,R",
#     "1:0,B",
#     "1:0,Y",
# ]
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

for opponent in game.opponents:
    print([str(i) for i in opponent.knowledge])
    print(len(opponent.card_potentials))