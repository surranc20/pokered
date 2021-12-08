import json
import random
from os.path import join
from .utils.managers.frameManager import FRAMES
from .utils.UI.drawable import Drawable
from .utils.vector2D import Vector2
from .move import Move
from .abilities import Ability


class Pokemon(Drawable):
    PLAYER_POKE_POS = Vector2(36, 48)
    ENEMY_POKE_POS = Vector2(148, 6)

    def __init__(self, pokemon_name, enemy=False, gender="male",
                 move_set=None):
        """Creates an instance of a pokemon. Requires the pokemon name in all
        lowercase as well as if the pokemon belongs to an enemy. Also requires
        the gender of the pokemon. Can provide a list of the pokemon's
        moves right in the constructor as well."""
        with open(join("jsons",
                       "pokemon_lookup.json"), "r") as pokemon_lookup_json:
            pokemon_lookup = json.load(pokemon_lookup_json)
            _lookup = tuple(pokemon_lookup[pokemon_name])
        _pos = self.PLAYER_POKE_POS if not enemy else self.ENEMY_POKE_POS
        _offset = _lookup if enemy else (_lookup[0] + 1, _lookup[1])
        self.name = pokemon_name
        self.nick_name = self.name.upper()
        self.gender = gender
        self.moves = []
        self.held_item = None
        self.ability = Ability("Static")
        self.nature = "Placeholder"
        self.exp = 100  # Placeholder
        self.nxt_lvl = 2000  # Placeholder

        # TODO: Fix the above exp and nxt_lvl variables

        # Keeps track of the status effects currently on the pokemon.
        self.status = []
        self.enemy = enemy
        self.stats = {
            "LVL": 62,
            "HP": 147,
            "Current HP": 147,
            "Attack": 49,
            "Defense": 49,
            "Sp. Attack": 100,
            "Sp. Defense": 117,
            "Speed": 45}

        # Summary image
        self.summary_image = \
            FRAMES.getFrame(join("pokemon", "pokemon_big.png"),
                            offset=_lookup)

        # Get the type of the pokemon.
        with open(join("jsons", "pokemon.json", encoding="utf-8"), "r") as \
                pokemon_json:
            pokemon = json.load(pokemon_json)
            pokemon_data = pokemon[pokemon_name.capitalize()]

        self.type = pokemon_data["type"]
        self.id_num = pokemon_data["id"]

        # Determines whether or not to draw the pokemon.
        self.can_draw = True

        # Add moves if given if passed in via constructor
        if move_set is not None:
            self.add_move_list(move_set)

        # Create drawable portion of the pokemon
        super().__init__(join("pokemon", "pokemon_big.png"),
                         Vector2(_pos.x, _pos.y), offset=_offset)

    def draw(self, draw_surface):
        """Draws the pokemon."""
        if self.can_draw:
            super().draw(draw_surface)

    def add_move_list(self, lyst):
        """Adds the move list to the pokemon."""
        for move in lyst:
            self.moves.append(Move(move))

    def add_status(self, status):
        """Adds a status effect to a pokemon."""
        self.status.append(status)

    def is_alive(self):
        """Returns if the pokmeon is alive."""
        return self.stats["Current HP"] != 0

    def add_move(self, move):
        """Adds a single move to the pokemon's moveset."""
        if len(self.moves) < 4:
            self.moves.append(move)

    def can_move(self):
        """Determines whether a pokemon's status ailments will allow it to
        move."""
        if "paralyze" in self.status:
            prob = random.randint(0, 100)
            if prob < 25:
                return "paralyze"
        return True

    @property
    def lvl(self):
        """Get the level of the pokemon."""
        return self.stats["LVL"]

    def __str__(self):
        """Allows a pokemon object to be printed."""
        return self.name

    def __repr__(self):
        """Used for debugging purposes primarily."""
        return self.name
