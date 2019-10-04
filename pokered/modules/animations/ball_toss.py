from os.path import join
from ..animated import Animated
from ..frameManager import FRAMES
from ..vector2D import Vector2


class BallToss(Animated):
    def __init__(self, position):
        super().__init__(join("battle", "pokeball_anim.png"), position)
        self._nFrames = 4
        self._framesPerSecond = 12