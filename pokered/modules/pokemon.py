import json
from os.path import join
from .utils.drawable import Drawable
from .utils.vector2D import Vector2
from .move import Move

class Pokemon(Drawable):
    PLAYER_POKE_POS = Vector2(36, 48)
    ENEMY_POKE_POS = Vector2(148, 6) 

    def __init__(self, pokemon_name, enemy=False, gender="male", move_set=None):
        with open(join("jsons", "pokemon_lookup.json"), "r") as pokemon_lookup_json:
            pokemon_lookup = json.load(pokemon_lookup_json)
            _lookup = tuple(pokemon_lookup[pokemon_name])
        _pos = self.PLAYER_POKE_POS if not enemy else self.ENEMY_POKE_POS
        _offset = _lookup if enemy else (_lookup[0] + 1, _lookup[1])
        self._name = pokemon_name
        self._nick_name = self._name
        self._gender = gender
        self._moves = []
        self._held_item = None
        self._ability = None
        self._status = []
        self._enemy = enemy
        self._stats = {
            "LVL" : 99,
            "HP": 168,
            "Current HP" : 168,
            "Attack": 49,
            "Defense": 49,
            "Sp. Attack": 65,
            "Sp. Defense": 117,
            "Speed": 45
        }

        with open(join("jsons", "pokemon.json"), "r") as pokemon_json:
            pokemon = json.load(pokemon_json)
            pokemon_data = pokemon[pokemon_name.capitalize()]

        self._type = pokemon_data["type"]

        if move_set != None:
            self.add_move_list(move_set)

        super().__init__(join("pokemon", "pokemon_big.png"), _pos, offset= _offset)
    
    def add_move_list(self, lyst):
        for move in lyst:
            self._moves.append(Move(move))

    def get_nick_name(self):
        return self._nick_name
    
    def get_name(self):
        return self._name
    
    def get_ability(self):
        return self._ability
    
    def get_status(self):
        return self._status
    
    def get_gender(self):
        return self._gender
    
    def get_moves(self):
        return self._moves
    
    def is_alive(self):
        return True
    
    def add_move(self, move):
        if len(self._moves) < 4:
            self._moves.append(move)
    
    def get_lvl(self):
        return self._stats["LVL"]
    
    def get_type(self):
        return self._type
    
    def get_held_item(self):
        return self._held_item

    def __str__(self):
        return self._name
    
    def __repr__(self):
        return self._name
