import random
from os.path import join
from ..move_base import MoveBase
from ....utils.soundManager import SoundManager

class IceShards(MoveBase):
    FRAME_LIST = []
    def __init__(self, attacker, defender, enemy=False):
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "ice_beam.png")
        self._fps = 10
        self._round_two = True
        self.pop_frame_list()
        SoundManager.getInstance().playSound(join("moves", "ice_beam_2.wav"))

    def pop_frame_list(self):
        for line in range(10):
            line = []
            for tup in range(random.randint(3,5)):
                tup = (2, (random.randint(145, 205), random.randint(20, 60)))
                line.append(tup)
            self.FRAME_LIST.append(line)