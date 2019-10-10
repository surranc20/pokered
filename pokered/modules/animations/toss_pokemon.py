from ..animated import AnimatedGroup
from .ball_toss import BallToss
from .poke_emerge import PokeEmerge
from .trainer_toss import TrainerToss
from ..pokemon import Pokemon
from ..vector2D import Vector2


class TossPokemon(AnimatedGroup):
    
    def __init__(self, pokemon_name, lead_off=False, enemy=False):
        if lead_off and not enemy: super().__init__([TrainerToss(Vector2(50, 48), 0), BallToss(Vector2(25,70), 1), PokeEmerge(Vector2(48, 55), pokemon_name, 2)], Pokemon(pokemon_name))
        elif not lead_off and not enemy: 
            print("here!!!!")
            super().__init__([BallToss(Vector2(25,70), 0), PokeEmerge(Vector2(48, 55), pokemon_name, 1)], Pokemon(pokemon_name))
        elif lead_off and enemy: pass
        else: super().__init__([BallToss(Vector2(165,61),0, enemy=True), PokeEmerge(Vector2(164, 13), pokemon_name, 1, enemy=True)], Pokemon(pokemon_name, enemy=True))