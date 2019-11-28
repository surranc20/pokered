from os.path import join
from .move_base import MoveBase
from ...utils.soundManager import SoundManager

class DoubleSlap(MoveBase):
    FRAME_LIST = [

    ]

    def __init__(self, attacker, defender, enemy=False):
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "body_slam.png")
        self._fps = 20
        SoundManager.getInstance().playSound(join("moves", "double_slap.wav"))