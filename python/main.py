import itertools as it
import re

direct_card_input = re.compile("(.*)\[(.*)\]")
ColorPossibilities = set(['R', 'B', 'Y', 'G'])
NumberPossibilities = set(['1', '2', '3'])
StonePossibilities = set(['D', 'O', 'P'])
deck = [i for i in it.product(ColorPossibilities, NumberPossibilities, StonePossibilities)]

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

def passes(state, knowledge: list[Knowledge], hand_size:int):
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

    facedown = state[0]
    players = state[1:]
    players_split = list(it.zip_longest(*[iter(players)] * hand_size))
    for element in knowledge:
        player = set(players_split[element.player_num-1])
        if explicit_card_missing(element, player):
            return False
        if has_invalid_non_cards(element, player):
            return False
        if question_asked_fail(element, player):
            return False
    return True


def process_cycle(all_states, knowledge, hand_size):
    working_states, all_states = it.tee(all_states)
    peek = (state for state in working_states if passes(state, knowledge, hand_size))
    state1 = next(peek, None)
    state2 = next(peek, None)
    del peek
    if state1 is None:
        print("Contradiction")
        raise Exception("Contradictory knowledge")
    if state2 is None:
        print("Solved!")
        return state1[0]
    return None, (state for state in all_states if passes(state, knowledge, hand_size))
            

def main(working_deck, hand_size):
    knowledge: list[Knowledge] = []
    all_states = it.permutations(working_deck, len(working_deck))
    while True:
        print("Send knowledge in format <Player Number>:<Number of cards>,<Question Asked>[<Comma Seperated Explicit Cards>]")
        new_know = input("  >")
        know = parse_new_knowledge(new_know)
        knowledge.append(know)
        working_states, all_states = it.tee(all_states)
        result, _ = process_cycle(working_states, knowledge, hand_size)
        if result:
            return result
def count(iterable):
    return sum(1 for _ in iterable)
    
def solver_mode(working_deck, hand_size, knowledge_lines):
    knowledge: list[Knowledge] = []
    all_states = it.permutations(working_deck, len(working_deck))
    final_states, all_states= it.tee(all_states)
    for line in knowledge_lines:
        know = parse_new_knowledge(line)
        knowledge.append(know)
        working_states, all_states = it.tee(all_states)
        result, final_states = process_cycle(working_states, knowledge, hand_size)
        if result:
            return result, final_states
    return None, final_states
    
bool_conv = {"false": False, "true": True}
if __name__ == "__main__":
    with open("INPUT.txt") as f:
        f_lines = [line for line in f]
    player_cards = [str_to_card_tup(i.strip()) for i in f_lines[0].split(",")]
    face_up = [str_to_card_tup(i.strip()) for i in f_lines[1].split(",")]
    hand_size = int(f_lines[2])
    working_deck = set(deck) - set(player_cards) - set(face_up)
    manual_mode = bool_conv[f_lines[3].lower()]
    if manual_mode:
        result = main(working_deck, hand_size)
        print(result)
    else:
        result, final_states = solver_mode(working_deck, hand_size, f_lines[4:])
        if not result:
            print("unable to actually solve")
            print("remaining results with current knowledge: ",end="")
            print(count(final_states))
        else:
            print(result)