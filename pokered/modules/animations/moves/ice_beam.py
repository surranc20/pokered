from os.path import join
from .move_base import MoveBase
from .generic.ice_shards import IceShards
from .generic.tint import Tint
from .generic.horizontal_jiggle import HorizontalJiggle
from .move_particle_system import MoveLinearParticleSystem
from ...utils.managers.soundManager import SoundManager

class IceBeam(MoveBase):

    def __init__(self, attacker, defender, enemy=False):
        """Displays the ice beam animation. This animation consists of two particle systems that
        generate crystals that follow a linear path towards the opponent. The player jiggles
        and is tinted while it is getting hit by the beam. The tint expires at the end of the move.
        Ice shards are played after the beam is done shooting. Extends MoveBase."""
        super().__init__(attacker, defender, enemy=enemy)
        self._move_file_name = join("moves", "ice_beam.png")
        self._fps = 20

        # Create and determine the direction of the crystal particle system
        if enemy:self._particle_systems = [MoveLinearParticleSystem(self._move_file_name, 1, (140, 70), 60, dx=-4, dy=2, duration=1), MoveLinearParticleSystem(self._move_file_name, 1, (140, 40), 60, dx=-4, dy=2, duration=1), MoveLinearParticleSystem(self._move_file_name, 2, (140, 55), 60, dx=-4, dy=2, particles_per_second=8, duration=1)]
        else: self._particle_systems = [MoveLinearParticleSystem(self._move_file_name, 1, (80, 100), 60, dx=4, dy=-2, duration=1), MoveLinearParticleSystem(self._move_file_name, 1, (80, 70), 60, dx=4, dy=-2, duration=1), MoveLinearParticleSystem(self._move_file_name, 2, (80, 85), 60, dx=4, dy=-2, particles_per_second=8, duration=1)]

        # Play the first part of the ice beam sound.
        SoundManager.getInstance().playSound(join("moves", "ice_beam_1.wav"))

        # Create the other sub animations
        self._part_one_over = False
        self._jiggle = HorizontalJiggle(defender)
        self._tint = Tint(defender, (173, 216, 230))

    def draw(self, draw_surface):
        """Draw each particle system as well and the tint. Also draws the ice shards after the beam has finished shooting."""
        self._tint.draw(draw_surface)
        for part_sys in self._particle_systems:
            part_sys.draw(draw_surface)

        # If the first half is over draw the ice shards animation.
        if self._part_one_over:
            self._shard_anim.draw(draw_surface)

    def update(self, ticks):
        """Updates each of the particle systems if they are active. Otherwise, updates the shard animation"""

        # If the particle systems are not dead update them.
        for part_sys in self._particle_systems:
            part_sys.update(ticks)
        self._particle_systems = [psys for psys in self._particle_systems if not psys.is_dead()]
        self._jiggle.update(ticks)

        # If the particle systems are dead and we have created the shard animation then update
        # the shard animation.
        if self._part_one_over:
            self._shard_anim.update(ticks)
            if self._shard_anim.is_dead(): self._is_dead = True

        # If the particle systems just finished create the shard animation here.
        # We must create it here and not at the start because otherwise the shard
        # sound would play at the beginning of the move.
        elif self._particle_systems == []:
            self._part_one_over = True
            self._shard_anim = IceShards(self._attacker, self._defender, enemy=self._enemy)
            self._jiggle.reset()