from os.path import join
from .move_base import MoveBase
from .generic.vertical_drop_and_recover import VerticalDropAndRecovery
from .generic.horizontal_lunge import HorizontalLunge
from .generic.horizontal_jiggle import HorizontalJiggle
from ...utils.managers.soundManager import SoundManager

class BodySlam(MoveBase):
    FRAME_LIST = [
        [(0, (160, 20))],
        [(0, (160, 20))],
        [(0, (160, 20))],
        []
    ]

    def __init__(self, attacker, defender, enemy=False):
        """This is the animation for the move body slam. It first performs a vertical drop and recover, then
        a horizontal lunge, then displays the impact png, the the enemy performs a horizontal lunge, then the enemy
        jiggles, then it lunges back to its start point and the animation ends. Extends MoveBase"""
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "body_slam.png")
        self._fps = 30

        # Create the sub animations
        self._drop = VerticalDropAndRecovery(attacker, 4)
        self._lunge = HorizontalLunge(attacker, 10 if not enemy else -10)
        self._reverse_lunge = HorizontalLunge(attacker, -10 if not enemy else 10)
        self._enemy_lunge = HorizontalLunge(defender, 14 if not enemy else -14)
        self._enemy_recover = HorizontalLunge(defender, -14 if not enemy else 14)
        self._oscillation_made = False
        self._displayed_png = False

        # Play body slam sound
        SoundManager.getInstance().playSound(join("moves", "body_slam.wav"))

        # This is one of the few animations where Move Base's attempt to adjust the frame_list's frame's
        # positions does not work well so we will do this manually. This makes sure that when the enemy
        # uses body slam the impact png will display to the right of the player's pokemon.
        if enemy:
            self.FRAME_LIST = [
                [(0, (175, 20))],
                [(0, (175, 20))],
                [(0, (175, 20))],
                []
            ]

    def update(self, ticks):
        """Updates the animation. Steps through the various sub animations."""

        # First finish the vertical drop and recover animation
        if not self._drop.is_dead():
            self._drop.update(ticks)

        # If the drop is done the attacker lunges
        elif not self._lunge.is_dead():
            self._lunge.update(ticks)

        # Once the lunge is over the impact sprite is displayed
        elif not self._displayed_png:
            super().update(ticks)

        # Once the impact sprite has been displayed the enemy is knocked (lunges)
        elif not self._enemy_lunge.is_dead():
            self._enemy_lunge.update(ticks)

        # Once the enemy has lunged it jiggles in place
        elif not self._oscillation.is_dead():
            self._oscillation.update(ticks)

        # Once the enemy is done jiggling the attacker lunges back to its start position
        elif not self._reverse_lunge.is_dead():
            self._reverse_lunge.update(ticks)

        # Once the attacker has returned to his start position the enemy returns to its start position
        elif not self._enemy_recover.is_dead():
            self._enemy_recover.update(ticks)

        # If every animation has played the animation is over
        else:
            self._is_dead = True


        # This resets the animations is_dead variable which gets flipped to true by super()
        # in the displaying png phase
        if self.is_dead() and not self._displayed_png:
            self._displayed_png = True
            self._is_dead = False

        # This creates the osciallation animation. It must be made here because it needs to be created
        # after the defending pokemon has been knocked into the position it will jiggle in.
        if self._enemy_lunge.is_dead() and not self._oscillation_made:
            self._oscillation = HorizontalJiggle(self._defender, .5)
            self._oscillation_made = True




