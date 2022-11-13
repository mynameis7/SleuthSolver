import itertools as it
import re

direct_card_input = re.compile("(.*)\[(.*)\]")

class Knowledge(object):
    def __init__(self, knowledge):
        player_num, num, question_asked, cards = knowledge
        self.player_num = player_num
        self.num = num
        self.question_asked = question_asked
        self.cards = cards

def str_to_card_tup(str_val):
    return (str_val[0], str_val[1], str_val[2])

def parse_new_knowledge(knowledge: str): #1:1,BD[R1P]
    player_num, real_knowledge = knowledge.split(":")
    num, b = real_knowledge.split(",")
    has_specific_cards = direct_card_input.match(b)
    card_tups = None
    question_asked = None
    if has_specific_cards:
        card_tups = [str_to_card_tup(_str) for _str in has_specific_cards.group(2).split(";")]
        question_asked = has_specific_cards.group(1)
    else:
        question_asked = b
    return Knowledge((player_num, num, question_asked, card_tups))

def passes(state, knowledge: list[Knowledge]):


def main():
    ColorPossibilities = set(['R', 'B', 'Y', 'G'])
    NumberPossibilities = set(['1', '2', '3'])
    StonePossibilities = set(['D', 'O', 'P'])
    deck = it.product(ColorPossibilities, NumberPossibilities, StonePossibilities)

    player_cards = set((str_to_card_tup(_str) for _str in ["R1D", "B3P","R2O", "Y3P", "G1D", "Y1O", "B2D","G3D"]))
    face_up = set((str_to_card_tup(_str) for _str in ["B2P", "Y1P", "G2P"]))
    deck = set(deck) - set(player_cards) - set(face_up)
    knowledge: list[Knowledge] = []
    states = [i for i in it.permutations(deck, len(deck))]
    while True:
        new_know = input()
        know = parse_new_knowledge(new_know)
        knowledge.append(know)
        states = [state for state in states if passes(state, knowledge)]


if __name__ == "__main__":
    main()