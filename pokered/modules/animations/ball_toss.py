from os.path import join
from ..utils.animated import AnimatedGroupPart
from ..utils.frameManager import FRAMES
from ..utils.vector2D import Vector2
from .poke_emerge import PokeEmerge


class BallToss(AnimatedGroupPart):
    def __init__(self, position, anim_sequence_pos, enemy=False):
        """BallToss is part of the animated group TossPokemon. It takes all the same arguments as
        an AnimatedGropuPart as well as an optional enemy argument. Enemy specifies who is throwing the
        pokeball. This is necessary because the animation changes based on who is throwing the pokeball."""
        self._enemy = enemy
        if not self._enemy: 
            super().__init__(join("battle", "pokeball_anim.png"), position, anim_sequence_pos)
            self._nFrames = 4
            self._framesPerSecond = 20

            # Coordinates of the balls parabolic arc
            self._parabola = [  (27, 68), (27, 68), (28, 66), (28, 66), (29, 65), (29, 65), 
            (30, 63), (30, 63), (31, 61), (31, 61), (32, 60), (32, 60), (33, 58), (33, 58), 
            (34, 56), (34, 56), (35, 54), (35, 54), (35, 53), (35, 53), (36, 51), (36, 51),
            (36, 51), (36, 52), (37, 52), (37, 53), (37, 54), (37, 56), (37, 56), (38, 58),
            (39, 60), (39, 60), (40, 62), (40, 62), (41, 64), (41, 66), (42, 68), (43, 70),
            (43, 72), (44, 74), (44, 76), (44, 79), (45, 80), (45, 81), (45, 83), (46, 83),
            (46, 87), (46, 90), (46, 93), (47, 97), (48, 99)]

        else: # The enemy is tossing the ball
            super().__init__(join("battle", "pokeball_open_anim.png"), position, anim_sequence_pos)
            self._nFrames = 3
            self._framesPerSecond = 10
            self._animate = False

            # When the enemy tosses the ball the ball just stays in one place
            self._parabola = [(168, 58)] * 30

        
    def __repr__(self):
        """"Returns the representation of any BallToss which is simply 'Ball Toss'
        Used for debugging purposes."""
        return "Ball Toss"

    def update(self, ticks):
        """"Adds to the update method of an AnimatedGroupPart. Specifically, it handles
        the change in position that takes place during the ball toss. Also handles the starting
        and stopping of the animation if the enemy is tossing the ball. Returns the index
        of the next AnimatedGroupPart when done. For BallToss this will always be PokeEmerge."""
        super().update(ticks)
        if self._enemy:
            if len(self._parabola) < 12:
                self.startAnimation()

            if self._frame == self._nFrames - 1:
                self.stopAnimation()

                return self._anim_sequence_pos + 1
        
        if len(self._parabola) != 0:
            self._position = self._parabola.pop(0)
        else: 
            self.kill()
            return self._anim_sequence_pos + 1
        