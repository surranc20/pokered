from os.path import join
from ..animated import Animated
from ..frameManager import FRAMES
from ..vector2D import Vector2


class BallToss(Animated):
    def __init__(self, position):
        super().__init__(join("battle", "pokeball_anim.png"), position)
        self._nFrames = 4
        self._framesPerSecond = 20
        self._parabola = [  (27, 68), (27, 68), (28, 66), (28, 66), (29, 65), (29, 65), 
        (30, 63), (30, 63), (31, 61), (31, 61), (32, 60), (32, 60), (33, 58), (33, 58), 
        (34, 56), (34, 56), (35, 54), (35, 54), (35, 53), (35, 53), (36, 51), (36, 51),
        (36, 51), (36, 52), (37, 52), (37, 53), (37, 54), (37, 56), (37, 56), (38, 58),
        (39, 60), (39, 60), (40, 62), (40, 62), (41, 64), (41, 66), (42, 68), (43, 70),
        (43, 72), (44, 74), (44, 76), (44, 79), (45, 80), (45, 81), (45, 83), (46, 83),
        (46, 87), (46, 90), (46, 93), (47, 97), (48, 99)]
    
    def update(self, ticks):
        super().update(ticks)
        if len(self._parabola) != 0:
            self._position = self._parabola.pop(0)
        else: 
            self.kill()
        