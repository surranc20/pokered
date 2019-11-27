from os.path import join
from .move_base import MoveBase
from .generic.ice_shards import IceShards
from .generic.tint import Tint
from .generic.horizontal_jiggle import HorizontalJiggle
from .move_particle_system import MoveLinearParticleSystem
from ...utils.soundManager import SoundManager

class IceBeam(MoveBase):

    def __init__(self, pokemon, enemy=False):
        super().__init__(enemy=enemy)
        self._move_file_name = join("moves", "ice_beam.png")
        self._fps = 20
        if enemy:self._particle_systems = [MoveLinearParticleSystem(self._move_file_name, 1, (140, 70), 60, dx=-4, dy=2, duration=1), MoveLinearParticleSystem(self._move_file_name, 1, (140, 40), 60, dx=-4, dy=2, duration=1), MoveLinearParticleSystem(self._move_file_name, 2, (140, 55), 60, dx=-4, dy=2, particles_per_second=8, duration=1)]
        else: self._particle_systems = [MoveLinearParticleSystem(self._move_file_name, 1, (80, 100), 60, dx=4, dy=-2, duration=1), MoveLinearParticleSystem(self._move_file_name, 1, (80, 70), 60, dx=4, dy=-2, duration=1), MoveLinearParticleSystem(self._move_file_name, 2, (80, 85), 60, dx=4, dy=-2, particles_per_second=8, duration=1)]
        SoundManager.getInstance().playSound(join("moves", "ice_beam_1.wav"))
        self._part_one_over = False
        self._jiggle = HorizontalJiggle(pokemon)
        self._tint = Tint(pokemon, (173, 216, 230))
        
    def draw(self, draw_surface):
        for part_sys in self._particle_systems:
            part_sys.draw(draw_surface)
    
        self._tint.draw(draw_surface)
        if self._part_one_over:
            self._shard_anim.draw(draw_surface)
    
    def update(self, ticks):
        for part_sys in self._particle_systems:
            part_sys.update(ticks)
        self._particle_systems = [psys for psys in self._particle_systems if not psys.is_dead()]
        self._jiggle.update(ticks)
        
        if self._part_one_over:
            self._shard_anim.update(ticks)
            if self._shard_anim.is_dead(): self._is_dead = True
        
        elif self._particle_systems == []:
            self._part_one_over = True
            self._shard_anim = IceShards(enemy=self._enemy)
            self._jiggle.reset()