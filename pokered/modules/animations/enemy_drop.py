from os.path import join
from ..animated import AnimatedGroupPart
from ..frameManager import FRAMES
from ..vector2D import Vector2

class EnemyDrop(AnimatedGroupPart):
    def __init__(self, position, anim_sequence_pos):
        super().__init__(join("battle", "gary_battle.png"), position, anim_sequence_pos)
        self._nFrames = 1
        self._framesPerSecond = 1
        self._initial_position = position

    def update(self, ticks):
        self.setPosition(self.getPosition() + Vector2(3, 0))
        if self.getPosition().x > self._initial_position.x + 4:
            if self.getPosition().x > 240: self.kill()
            return self._anim_sequence_pos + 1
        

