from os.path import join
from .move_base import MoveBase
from .generic.vertical_drop_and_recover import VerticalDropAndRecovery
from .generic.horizontal_lunge import HorizontalLunge
from .generic.horizontal_jiggle import HorizontalJiggle
from ...utils.soundManager import SoundManager

class BodySlam(MoveBase):
    FRAME_LIST = [
        [(0, (160, 20))],
        [(0, (160, 20))],
        [(0, (160, 20))],
        [(0, (160, 20))],
        []
    ]

    def __init__(self, attacker, defender, enemy=False):
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "body_slam.png")
        self._drop = VerticalDropAndRecovery(attacker, 4)
        self._lunge = HorizontalLunge(attacker, 10 if not enemy else -10)
        self._reverse_lunge = HorizontalLunge(attacker, -10 if not enemy else 10)
        self._enemy_lunge = HorizontalLunge(defender, 14 if not enemy else -14)
        self._enemy_recover = HorizontalLunge(defender, -14 if not enemy else 14)
        self._oscillation_made = False
        self._displayed_png = False
        self._fps = 30
        SoundManager.getInstance().playSound(join("moves", "body_slam.wav"))
    
    def update(self, ticks):
        if not self._drop.is_dead():
            self._drop.update(ticks)
        elif not self._lunge.is_dead():
            self._lunge.update(ticks)
        elif not self._displayed_png:
            super().update(ticks)
        elif not self._enemy_lunge.is_dead():
            self._enemy_lunge.update(ticks)
        elif not self._oscillation.is_dead():
            self._oscillation.update(ticks)
        elif not self._reverse_lunge.is_dead():
            self._reverse_lunge.update(ticks)
        elif not self._enemy_recover.is_dead():
            self._enemy_recover.update(ticks)
        else:
            self._is_dead = True
        
        if self.is_dead() and not self._displayed_png:
            self._displayed_png = True
            self._is_dead = False
        
        if self._enemy_lunge.is_dead() and not self._oscillation_made:
            self._oscillation = HorizontalJiggle(self._defender, .5)
            self._oscillation_made = True


        

    