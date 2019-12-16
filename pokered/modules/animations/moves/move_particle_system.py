import random
from ...utils.UI.drawable import Drawable


class MoveLinearParticleSystem():
    def __init__(self, file_name, index_pos, start_pos, total_x_displacement,
                 dx=1, dy=-1, particles_per_second=10, duration=100):
        """Creates a particle system. Used in moves like ice beam. Takes as
        its input a file_name which specefies which file to look in for the
        individual particles. The index_pos which specifies the x offset to
        use in order to find the correct particle sprite. The start pos which
        specifies the start position of the particles The total x displacement
        that a particle will travel before dying. The dx and dy which
        specefies how much the particles position changes per update.
        Particles per second which determines how many particles spawn per
        second, and the duration in seconds for how long the system will
        last."""
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
        """Returns whether or not the particle system is dead"""
        return self._duration_timer > self._duration

    def draw(self, draw_surface):
        """Draws all the particles in the particle system"""
        for particle in self._particles:
            particle.draw(draw_surface)

    def update(self, ticks):
        """Updates all of the particles"""
        # Get rid of dead particles and increase timers
        self._particles = [particle for particle in self._particles
                           if not particle.is_dead()]
        self._respawn_timer += ticks
        self._duration_timer += ticks

        # Create a new particle if it is time
        if self._respawn_timer > 1 / self._particles_per_second:
            self._respawn_timer -= 1 / self._particles_per_second
            self._particles.append(Particle(self._file_name, self._index_pos,
                                            self._start_pos,
                                            self._total_x_displacement))

        # Update each particle in the system
        for particle in self._particles:
            particle.update(ticks, self._dx, self._dy)


class Particle(Drawable):
    def __init__(self, file_name, index_pos, start_pos, total_x_displacement):
        """Creates a particle for a particle system. Takes as input a file
        name and index pos which are used to get the particle sprite, the
        start pos of the sprite, and the total x displacement the sprite will
        travel before starting its death timer. If the index pos is a tuple of
        numbers then a random index will be chosen."""
        self._total_x_displacement = total_x_displacement
        self._start_pos = start_pos
        self._is_dead = False

        # Keeps track of how long a particle has been at its end position
        self._death_timer = 0

        # Randomly choose a sprite for the particle if index_pos is a tuple of
        # possible indices.
        if type(index_pos) == tuple:
            index_pos = random.choice(index_pos)

        super().__init__(file_name, start_pos, offset=(index_pos, 0))

    def update(self, ticks, dx, dy):
        """Updates the position of the particle based on dx and dy. Kills the particle
        if it has been stationary for more the .02 seconds"""

        # Move particle untill it has traveled the total x displacement
        if not abs(self._position[0] - self._start_pos[0]) > \
                self._total_x_displacement:
            self._position = (self._position[0] + dx, self._position[1] + dy)

        # Start death timer and kill particle if death timer is more than .02
        # seconds.
        else:
            self._death_timer += ticks
            if self._death_timer > .02:
                self._is_dead = True

    def is_dead(self):
        """Returns whether or not the particle is dead"""
        return self._is_dead
