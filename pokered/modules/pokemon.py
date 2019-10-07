from os.path import join
from .drawable import Drawable
from .vector2D import Vector2


class Pokemon(Drawable):
    PLAYER_POKE_POS = Vector2(46, 48)
    ENEMY_POKE_POS = Vector2(148, 6)
    POKEMON_LOOKUP = {"pikachu" : (6,3)}

    def __init__(self, pokemon_name, trainer="player"):
        _pos = self.PLAYER_POKE_POS if trainer == "player" else self.ENEMY_POKE_POS
        _lookup = self.POKEMON_LOOKUP[pokemon_name]
        _offset = _lookup if trainer != "player" else (_lookup[0] + 1, _lookup[1])
        self._name = pokemon_name
        super().__init__(join("pokemon", "pokemon_big.png"), _pos, offset= _offset)
        

    def __str__(self):
        return self._name