from ..utils.UI.animated import AnimatedGroup
from ..utils.vector2D import Vector2
from ..pokemon import Pokemon
from .ball_toss import BallToss
from .poke_emerge import PokeEmerge
from .trainer_toss import TrainerToss
from .enemy_drop import EnemyDrop


class TossPokemon(AnimatedGroup):
    def __init__(self, pokemon_name, trainer, lead_off=False, enemy=False):
        """AnimatedGroup containing all of the Animations that make up a
        trainer tossing a pokemon out onto the battle field. Arguments include
        pokemon_name so that PokeEmerge knows which pokemon to animate,
        lead_off so that it knows whether or not to include TrainerToss /
        EnemyDrop, and enemy so that its various parts can animate
        correctly."""
        if lead_off and not enemy:
            super().__init__([TrainerToss(Vector2(50, 48), 0),
                             BallToss(Vector2(25, 70), 1),
                             PokeEmerge(Vector2(48, 55), pokemon_name, 2)],
                             Pokemon(pokemon_name))
        elif not lead_off and not enemy:
            super().__init__([BallToss(Vector2(25, 70), 0),
                             PokeEmerge(Vector2(48, 55), pokemon_name, 1)],
                             Pokemon(pokemon_name))
        elif lead_off and enemy:
            super().__init__([EnemyDrop(Vector2(148, 6), 0, trainer),
                             BallToss(Vector2(165, 61), 1, enemy=True),
                             PokeEmerge(Vector2(164, 13), pokemon_name, 2,
                                        enemy=True)],
                             Pokemon(pokemon_name, enemy=True))
        else:
            super().__init__([BallToss(Vector2(165, 61), 0, enemy=True),
                             PokeEmerge(Vector2(164, 13), pokemon_name, 1,
                                        enemy=True)],
                             Pokemon(pokemon_name, enemy=True))
