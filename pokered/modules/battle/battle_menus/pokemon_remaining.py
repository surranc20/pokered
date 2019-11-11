from os.path import join
from ...utils.animated import AnimatedGroup, AnimatedGroupPart
from ...utils.vector2D import Vector2

class PokemonRemaining(AnimatedGroup):

    PLAYER_POSITION = Vector2(156,85)
    ENEMY_POSITION = Vector2(26,33)

    def __init__(self, player):
        """This is the little bar that has six pokeballs and indicates how many pokemon
        are left in you or your opponents party. Extends AnimatedGroup to inherit some of the
        functionality of that class even though nothing here is truly an animation."""
        self._is_enemy = player.is_enemy()
        self._total_pokemon = len(player.get_pokemon_team())
        self._total_pokemon_alive = len([pokemon for pokemon in player.get_pokemon_team() if pokemon.is_alive()])
        self._total_pokemon_dead = self._total_pokemon - self._total_pokemon_alive
        self._total_empty_spots = 6 - self._total_pokemon
        super().__init__(self._create_animations_list(), all_on=True)

    def _create_animations_list(self):
        """Helper method that fills the animations list of the AnimatedGroup with the correct pokeballs
        based on the health status of each pokemon in the party"""

        anims = []
        anim_sequence_pos = 1
        position = self.ENEMY_POSITION if self._is_enemy else self.PLAYER_POSITION
        anims.append(PokeballRemainingContainer(self._is_enemy))
        for status in [("empty", self._total_empty_spots), ("alive", self._total_pokemon_alive), ("dead", self._total_pokemon_dead)]:
            for ball in range(status[1]):
                anims.append(PokeballRemainingBall(status[0], position ,anim_sequence_pos))
                anim_sequence_pos += 1
                position = (position[0] + 10, position[1])
        return anims


class PokeballRemainingBall(AnimatedGroupPart):
    """Simple AnimatedGroupPart which is just an image of either an empty, colored, or greyed-out pokeball"""
    def __init__(self,pokeball_status, position, anim_sequence_pos):
        if pokeball_status == "empty": offset = (0, 0)
        elif pokeball_status == "dead": offset = (2, 0)
        else: offset = (1, 0)
        
        super().__init__(join("battle", "pokemon_remaining_balls.png"), position, anim_sequence_pos, offset=offset)

    
    def update(self, ticks):
        pass

class PokeballRemainingContainer(AnimatedGroupPart):
    """Simple AnimatedGroupPart which contains the container that appears on screen and
    holds the balls"""

    PLAYER_POSIITON = Vector2(136, 85)
    ENEMY_POSITION = Vector2(0,33)

    def __init__(self, is_enemy):
        pos =  self.ENEMY_POSITION if is_enemy else self.PLAYER_POSIITON
        offset = (0,0) if is_enemy else (0,1)
        print(offset)
        super().__init__(join("battle", "pokemon_remaining.png"), pos, 0, offset=offset)
    
    def update(self, ticks):
        pass
    

