from os.path import join
import json
import random


class Move:
    def __init__(self, move_name):
        """Creates an instance of a pokemon move."""
        # Load the moves info from moves.json
        with open(join("jsons", "moves.json"), "r") as moves_json:
            moves = json.load(moves_json)
            move = moves[move_name]
        self.move_name = move_name
        self.move_type = move["Move type"]
        self.category = move["Category"]
        self.accuracy = move["Accuracy"]
        self.move_power = move["Move power"]
        self.max_pp = move["PP"]
        self.current_pp = move["PP"]
        self.effect_accuracy = move["Effect Accuracy"]
        self.effects = move["Effects"]

    def get_num_hits(self):
        """If the move is a multi hit move then return the total number of
        hits the move will make in the current turn. Otherwise just
        return 1."""
        with open(join("jsons", "moves.json"), "r") as moves_json:
            moves = json.load(moves_json)
            multi = moves["Multi"]
        if multi.get(self.move_name, "Not") == "Not":
            return 1
        else:
            prob = random.random() * 100
            prob_dict = multi[self.move_name]
            for x in range(2, len(prob_dict) + 2):
                if prob <= prob_dict[str(x)]:
                    return x
                else:
                    prob -= prob_dict[str(x)]
            raise Exception

    def reset_pp(self):
        """Refills the move's pp."""
        self.current_pp = self.max_pp






