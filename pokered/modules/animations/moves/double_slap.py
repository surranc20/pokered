from os.path import join
from .move_base import MoveBase
from ...utils.managers.soundManager import SoundManager

class DoubleSlap(MoveBase):
    FRAME_LIST = [
        [(0, (170, 20))],
        [(0, (170, 20))],
        [(0, (170, 20))],
        [(0, (170, 20))],
        [],
        [],
        [],
        []
    ]

    def __init__(self, attacker, defender, enemy=False):
        """This displays the double slap animation. Extends MoveBase"""
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "body_slam.png")
        self._fps = 20

        # Plays double slap sound
        SoundManager.getInstance().playSound(join("moves", "double_slap.wav"))