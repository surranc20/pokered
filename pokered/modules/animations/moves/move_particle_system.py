import random
from ...utils.drawable import Drawable
from ...utils.vector2D import Vector2

class MoveLinearParticleSystem():
    def __init__(self, file_name, index_pos, start_pos, total_x_displacement, dx=1, dy=-1, particles_per_second=10, duration = 100):
        self._file_name = file_name
        self._index_pos = index_pos
        self._start_pos = start_pos
        self._total_x_displacement = total_x_displacement
        self._dx = dx
        self._dy = dy
        self._duration = duration
        self._respawn_timer = 0
        self._duration_timer = 0
        self._particles_per_second = particles_per_second
        self._particles = []

    
    def is_dead(self):
        return self._duration_timer > self._duration

    def draw(self, draw_surface):
        for particle in self._particles:
            particle.draw(draw_surface)
    
    def update(self, ticks):
        self._particles = [particle for particle in self._particles if not particle.is_dead()]
        self._respawn_timer += ticks
        self._duration_timer += ticks
        if self._respawn_timer > 1 / self._particles_per_second:
            self._respawn_timer -= 1 / self._particles_per_second
            self._particles.append(Particle(self._file_name, self._index_pos, self._start_pos, self._total_x_displacement))
        
        for particle in self._particles:
            particle.update(ticks, self._dx, self._dy)

class Particle(Drawable):
    def __init__(self, file_name, index_pos, start_pos, total_x_displacement):
        self._total_x_displacement = total_x_displacement
        self._start_pos = start_pos
        self._death_timer = 0
        self._is_dead = False
        if type(index_pos) == tuple:
            index_pos = random.choice(index_pos)
        super().__init__(file_name, start_pos, offset= (index_pos, 0))
    
    def update(self, ticks, dx, dy):
        if not abs(self._position[0] - self._start_pos[0]) > self._total_x_displacement:
            self._position = (self._position[0] + dx, self._position[1] + dy)
        else:
            self._death_timer += ticks
            if self._death_timer > .02:
                self._is_dead = True



    def is_dead(self):
        return self._is_dead