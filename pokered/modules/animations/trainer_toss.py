from os.path import join
from ..animated import AnimatedGroupPart
from ..frameManager import FRAMES
from ..vector2D import Vector2


class TrainerToss(AnimatedGroupPart):
    def __init__(self, position, anim_sequence_pos):
        super().__init__(join("battle", "trainer_toss_anim.png"), position, anim_sequence_pos)
        self._nFrames = 5
        self._framesPerSecond = 12
    
    def __repr__(self):
            return "trainer toss"
    
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
                return self._anim_sequence_pos + 1

            if self._flip: self._image = pygame.transform.flip(self._image, True, False)
        
        if self.getPosition().x + self._image.get_width() < 0:
            self.kill()

            
        return False


        