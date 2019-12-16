from os.path import join
from ..utils.UI.animated import AnimatedGroupPart
from ..utils.managers.frameManager import FRAMES
from ..utils.vector2D import Vector2


class TrainerToss(AnimatedGroupPart):
    def __init__(self, position, anim_sequence_pos):
        """First part of the AnimatedGroup Toss_Pokmeon. Moves trainer image to the left
        and once its position reaches a certain threshold it begins its animation."""
        super().__init__(join("battle", "trainer_toss_anim.png"), position, anim_sequence_pos)
        self._nFrames = 5
        self._framesPerSecond = 12

    def __repr__(self):
        """Returns the representation of TrainerToss. Simply 'Trainer Toss'"""
        return "Trainer Toss"

    def update(self, ticks):
        """Overides the update method of AnimatedGroupPart. Controls position
        and animation."""

        #TODO: Maybe utilize ticks here for a more consistent sweep?
        # Animation always moves 2 pixels to the left per update call
        self.setPosition(self.getPosition() - Vector2(2, 0))

        # Trainer stops animating for a time when he cocks his arm back
        if self._frame == 1:
            self._animate = False

        # Once the trainer is about to travel off screen he begins animating again
        if self.getPosition().x < 2 and self._frame == 1:
            self._animate = True

        # Simnple animation loop
        if self._animate:
         self._animationTimer += ticks

         if self._animationTimer > 1 / self._framesPerSecond:
            self._frame += 1
            self._frame %= self._nFrames
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))

            # If the animation is on the last frame then stop animating and
            # return the index of the next AnimatedGroupPart. In this case that is
            # the index of a BallToss.
            if self._frame == self._nFrames - 1:
                self._animate = False
                return self._anim_sequence_pos + 1

            #TODO: Figure out why I put this here
            if self._flip: self._image = pygame.transform.flip(self._image, True, False)

        # Once TrainerToss is off screen it kills itself.
        if self.getPosition().x + self._image.get_width() < 0:
            self.kill()

        return False


