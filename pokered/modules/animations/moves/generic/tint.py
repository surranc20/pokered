import pygame
class Tint():
    def __init__(self, pokemon, color):
        self._pokemon = pokemon 
        self._is_dead = False
        self._tint = pygame.Surface((64,64))
        self._tint.set_colorkey((0,0,0))
        pygame.transform.threshold(self._tint, pokemon._image, pokemon._image.get_colorkey(), set_color=color)  
        self._tint.set_alpha(200)

    def draw(self, draw_surface):
        print(self._pokemon._position)
        draw_surface.blit(self._tint, (self._pokemon._position.x, self._pokemon._position.y))  
    
    def is_dead(self):
        return self._is_dead
    
    
