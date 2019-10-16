from os.path import join
from ..animated import AnimatedGroupPart
from ..frameManager import FRAMES
from ..vector2D import Vector2

class EnemyDrop(AnimatedGroupPart):
    def __init__(self, position, anim_sequence_pos):
        """"This is enemies equivalent of a TrainerToss. The enemy simply moves right off the screen"""
        super().__init__(join("battle", "gary_battle.png"), position, anim_sequence_pos)
        self._nFrames = 1
        self._framesPerSecond = 1
        self._initial_position = position

    def update(self, ticks):
        """Player moves two pixels per update method. Returns the index of the next AnimatedGroupPart when done.
        In this case that Will always be BallToss."""
        #TODO: Maybe change this so that it utilizes ticks to determine how far to move enemy?
        self.setPosition(self.getPosition() + Vector2(2, 0))
        if self.getPosition().x > self._initial_position.x + 4:
            if self.getPosition().x > 240: self.kill()
            return self._anim_sequence_pos + 1
        

