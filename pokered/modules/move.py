from os.path import join
import json

class Move:
    def __init__(self, move_name):
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
        self.effects = move["Effects"]
    


