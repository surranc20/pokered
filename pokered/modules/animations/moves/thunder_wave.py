from os.path import join
from .move_base import MoveBase
from ...utils.managers.soundManager import SoundManager


class ThunderWave(MoveBase):
    FRAME_LIST = [
        [(2, (180, -20))],
        [(2, (180, -20)), (2,  (180, 0))],
        [(2, (180, -20)), (2,  (180, 0)), (2,  (180, 12))],
        [(2, (180, -20)), (2,  (180, 0)), (2,  (180, 12)), (2,  (180, 32))],
        [(2, (180, -20)), (2,  (180, 0)), (2,  (180, 12)), (2,  (180, 32)),
            (2, (180, 40))],
        [(2,  (180, 0)), (2,  (180, 12)), (2,  (180, 32)), (2,  (180, 40))],
        [(2,  (180, 12)), (2,  (180, 32)), (2,  (180, 40))],
        [(2,  (180, 32)), (2,  (180, 40))],
        [(2,  (180, 40))],
        [],
        [],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [(2, (155, 25), "r"), (3, (177, 25), "r")],
        [(2, (155, 35), "r"), (3, (177, 35), "r")],
        [(2, (155, 45), "r"), (3, (177, 45), "r")],
        [],
        []
    ]
    SECONDARY_FRAME_LIST = [
        [(0, (165, 50)), (0, (190, 55), "h"), (1, (175, 30))],
        [(0, (162, 51), "h"), (0, (185, 52), "v"), (1, (175, 30), "v")],
        [(0, (167, 48), "h"), (0, (182, 54), "v"), (1, (175, 30), "v")],
        [(0, (170, 60)), (0, (187, 53), "h"), (1, (167, 38), "h")],
        [(0, (165, 50)), (0, (185, 55), "h"), (1, (175, 30))],
        [],
        [],
        []
    ]

    def __init__(self, attacker, defender, enemy=False):
        """Creates the thunder wave animation. I experimented with a different
        way of getting sprites from two different sheets here. Once the first
        frame list is finished it goes to the secondary frame list and changes
        the sprite sheet."""
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "thunder_wave.png")
        self._fps = 20
        self._round_two = True
        SoundManager.getInstance().playSound(join("moves", "thunder_wave.wav"))

    def update(self, ticks):
        """Updates the thunder wave animation. After the first frame list is
        complete it transitions to the secondary frame list and changes the
        fps. Once that is done the move is over."""
        super().update(ticks)
        if self.is_dead() and self.FRAME_LIST != self.SECONDARY_FRAME_LIST \
                and self._round_two:
            self._is_dead = False
            self._round_two = False
            self.FRAME_LIST = self.SECONDARY_FRAME_LIST
            self._frame_num = 0
            self._fps = 10
            self._move_file_name = join("moves", "thunderbolt_static.png")
