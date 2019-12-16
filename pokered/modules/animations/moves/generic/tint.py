import pygame


class Tint():
    def __init__(self, pokemon, color):
        """This animation tints the pokemon sprite for a given time.
        In addition to a pokemon, this animation also takes a color as
        an input. Used in moves like ice beam."""
        self._pokemon = pokemon
        self._is_dead = False

        # Create the tint surface so that it only maps to the non transparent
        # pixels of the pokemon
        self._tint = pygame.Surface((64, 64))
        self._tint.set_colorkey((0, 0, 0))
        pygame.transform.threshold(self._tint, pokemon._image,
                                   pokemon._image.get_colorkey(),
                                   set_color=color)

        # Make tint transparent so details of the pokemon can still be seen
        self._tint.set_alpha(200)

    def draw(self, draw_surface):
        """Draws the tint surface right over the pokemon sprite to achieve
        tint affect."""
        draw_surface.blit(self._tint,
                          (self._pokemon._position.x,
                           self._pokemon._position.y))

    def is_dead(self):
        """Returns whether or not the animation is over. In this instance,
        the is_dead variable will need to be changed by an actual move in
        order to trigger the end of the tint animation."""
        return self._is_dead
