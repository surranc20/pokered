from os.path import join
from .move_base import MoveBase
from ...utils.soundManager import SoundManager


class Thunderbolt(MoveBase):
    FRAME_LIST = [
        [(0, (200, 0))],
        [(0, (200, 0)), (0, (200, 12))],
        [(0, (200, 0)), (0, (200, 12)), (1, (200, 40))], 
        [(0, (160, 0)), (0, (200, 0)), (0, (200, 12)), (1, (200, 40))],
        [(0, (160, 0)), (0, (160, 12)), (0, (200, 12)), (1, (200, 40))],
        [(0, (160, 0)), (0, (160, 12)), (1, (160, 32)), (1, (200, 40)), (2, (180, -20))],
        [(0, (160, 0)), (0, (160, 12)), (1, (160, 32)), (1, (160, 40)), (2, (180, -20))],
        [(0, (160, 0)), (0, (160, 12)), (1, (160, 32)), (1, (160, 40)), (2, (180, -20)), (2,  (180, 0))],
        [(0, (160, 12)), (1, (160, 32)), (1, (160, 40)), (2, (180, -20)), (2,  (180, 0))],
        [(1, (160, 32)), (1, (160, 40)), (2, (180, -20)), (2,  (180, 0)), (2,  (180, 12))],
        [(1, (160, 40)), (2, (180, -20)), (2,  (180, 0)), (2,  (180, 12)), (2,  (180, 32))],
        [(2, (180, -20)), (2,  (180, 0)), (2,  (180, 12)), (2,  (180, 32)), (2,  (180, 40))],
        [(2,  (180, 0)), (2,  (180, 12)), (2,  (180, 32)), (2,  (180, 40))],
        [(2,  (180, 12)), (2,  (180, 32)), (2,  (180, 40))],
        [(2,  (180, 32)), (2,  (180, 40))],
        [(2,  (180, 40))], 
        [],
        [],
        []
    ]
    SECONDARY_FRAME_LIST = [
        [(0, (170, 40))],
        [(0, (170, 40), 'h')],
        [(1, (170, 40))],
        [(0, (170, 40))],
        [(1, (170, 40))],
        [(1, (170, 40), 'h')],
        []

    ]
    TERTIARY_FRAME_LIST = [
        [(0, (165, 50)), (0, (190, 55), "h"), (1, (175, 30))],
        [(0, (162, 51), "h"), (0, (185, 52), "v"), (1, (175, 30), "v")],
        [(0, (167, 48), "h"), (0, (182, 54), "v"), (1, (175, 30), "v")],
        [(0, (170, 60)), (0, (187, 53), "h"), (1, (167, 38), "h")],
        [(0, (165, 50)), (0, (185, 55), "h"), (1, (175, 30))],
        [],
        [],
        []
        
    ]
    def __init__(self, enemy=False):
        super().__init__(enemy=enemy)
        self._move_file_name = join("moves", "thunderbolt.png")
        self._fps = 20
        self._round_two = True
        SoundManager.getInstance().playSound(join("moves", "thunderbolt.wav"))

    def update(self, ticks):
        super().update(ticks)
        if self.is_dead() and self.FRAME_LIST != self.SECONDARY_FRAME_LIST and self._round_two:
            self._is_dead = False
            self._round_two = False
            self.FRAME_LIST = self.SECONDARY_FRAME_LIST
            self._frame_num = 0
            self._fps = 10
            self._move_file_name = join("moves", "thunderbolt_ball.png")
        

        if self.is_dead() and self.FRAME_LIST != self.TERTIARY_FRAME_LIST:
            self._is_dead = False
            self.FRAME_LIST = self.TERTIARY_FRAME_LIST
            self._frame_num = 0
            self._fps = 6
            self._move_file_name = join("moves", "thunderbolt_static.png")