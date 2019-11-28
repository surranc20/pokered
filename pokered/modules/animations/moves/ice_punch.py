from os.path import join
from .move_base import MoveBase
from .generic.ice_shards import IceShards
from .generic.tint import Tint
from ...utils.soundManager import SoundManager
import math

class IcePunch(MoveBase):
    FRAME_LIST = [

    ]

    def __init__(self, attacker, defender, enemy=False):
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "ice_punch.png")
        self._fps = 45
        self._round_two = True
        SoundManager.getInstance().playSound(join("moves", "ice_punch.wav"))
        self.create_square()
        self._transfer_num = len(self.FRAME_LIST)
        self.create_punch()
        self._tint = Tint(defender, (173, 216, 230))
        self._part_one_over = False
        

    def create_punch(self):
        self.FRAME_LIST.append([(0, (170, 30))])
        self.FRAME_LIST.append([(0, (170, 30))])
        self.FRAME_LIST.append([(0, (170, 30))])
        self.FRAME_LIST.append([(0, (170, 30))])
        
        
    def draw(self, draw_surface):
        if not self._part_one_over:
            super().draw(draw_surface)
        self._tint.draw(draw_surface)
        if self._part_one_over:
            self._shard_anim.draw(draw_surface)

    def update(self, ticks):
        if not self._part_one_over:
            super().update(ticks)
        if self._frame_num == self._transfer_num:
            self._move_file_name = join("moves", "fist.png")

        if self._part_one_over:
            self._shard_anim.update(ticks)
            if self._shard_anim.is_dead(): self._is_dead = True
        
        elif self.is_dead():
            self._part_one_over = True
            self._is_dead = False
            self._shard_anim = IceShards(self._attacker, self._defender, enemy=self._enemy)
            for line in self._shard_anim.FRAME_LIST:
                print(line)

        



    def create_square(self):
        
        lyst = [(120, 20), (200, 20), (120, 100), (200, 100)]

        for x in range(20):
            x1, x2, y1, y2 = lyst[0][0], lyst[1][0], lyst[0][1], lyst[3][1]
            midx, midy = (x1 + x2) / 2, (y1 + y2) / 2
            points = []
            frame = []
             
            for corner in lyst:

                tempx = corner[0] - midx
                tempy = corner[1] - midy

                rotatedx = tempx * math.cos(45) - tempy * math.sin(45)
                rotatedy = tempx * math.sin(45) + tempy * math.cos(45)

                x = rotatedx + midx
                y = rotatedy + midy

                points.append((x,y))
                frame.append((1, (math.floor(x),math.floor(y))))
            self.FRAME_LIST.append(frame)
            lyst = self.make_smaller(points)

    def make_smaller(self, points):
        x = []
        y = []


        

        for point in points:
            x.append(point[0])
            y.append(point[1])
        
        sortx = x.copy()
        sorty = y.copy()

        sortx.sort()
        sorty.sort()


        small_x = sortx[0:2]
        big_x = sortx[2:]

        small_y = sorty[0:2]
        big_y = sorty[2:]

        new_x =[]
        for num in x:
            if num in small_x:
                new_x.append(num + 2)
            else:
                new_x.append(num - 2)
        
        new_y = []
        for num in y:
            if num in small_y:
                new_y.append(num + 2)
            else:
                new_y.append(num - 2)

        return [(new_x[0], new_y[0]), (new_x[1], new_y[1]), (new_x[2], new_y[2]), (new_x[3], new_y[3])]




