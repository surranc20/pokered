import random
from os.path import join
from ..move_base import MoveBase
from ....utils.managers.soundManager import SoundManager


class IceShards(MoveBase):
    FRAME_LIST = []

    def __init__(self, attacker, defender, enemy=False):
        """This animation displays the shards that appear after some
        ice moves."""

        # We need to reset the frame list here because the FRAME_LIST
        # will increase each time a new IceShard animation is created.
        # This happens becuase the ice shard animation is generated dynamically
        # and then added to the class variable FRAME_LIST to leverage the move
        # base framework.
        self.FRAME_LIST = []
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "ice_beam.png")
        self._fps = 10
        self._round_two = True
        self.pop_frame_list()

        # Plays ice shard sound
        SoundManager.getInstance().playSound(join("moves", "ice_beam_2.wav"))

    def pop_frame_list(self):
        """Randomly populate the FRAME_LIST with a sequence of ice crystals. Creates
        10 different total frames each consisting of 3-5 crystals
        in a random location."""
        for line in range(10):
            line = []
            for tup in range(random.randint(3, 5)):
                tup = (2, (random.randint(145, 205), random.randint(20, 60)))
                line.append(tup)
            self.FRAME_LIST.append(line)
