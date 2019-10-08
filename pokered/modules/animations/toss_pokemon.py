from ..animated import AnimatedGroup
from .ball_toss import BallToss
from .poke_emerge import PokeEmerge
from .trainer_toss import TrainerToss
from ..pokemon import Pokemon
from ..vector2D import Vector2


class TossPokemon(AnimatedGroup):
    def __init__(self, pokemon_name):
        super().__init__([TrainerToss(Vector2(50, 48), 0), BallToss(Vector2(25,70), 1), PokeEmerge(Vector2(48, 55), pokemon_name, 2)], Pokemon(pokemon_name))