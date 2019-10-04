from os.path import join
from ..animated import Animated
from ..frameManager import FRAMES
from ..vector2D import Vector2
from .ball_toss import BallToss


class TrainerToss(Animated):
    def __init__(self, position):
        super().__init__(join("battle", "trainer_toss_anim.png"), position)
        self._nFrames = 5
        self._framesPerSecond = 12
    
    def update(self, ticks):
        self.setPosition(self.getPosition() - Vector2(2, 0))

        if self._frame == 1:
            self._animate = False

        if self.getPosition().x < 2 and self._frame == 1: 
            self._animate = True

        if self._animate:
         self._animationTimer += ticks
         
         if self._animationTimer > 1 / self._framesPerSecond:
            self._frame += 1
            self._frame %= self._nFrames
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
            if self._frame == self._nFrames - 1: 
                self._animate = False
                return BallToss(Vector2(25,70))

            if self._flip: self._image = pygame.transform.flip(self._image, True, False)

            
        return False