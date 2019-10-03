from os.path import join
from ..animated import Animated

class TrainerToss(Animated):
    def __init__(self, position):
        super().__init__(join("battle", "trainer_toss_anim.png"), position)
        self._nFrames = 5
        self._framesPerSecond = 5
