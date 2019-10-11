import pygame
from os.path import join
from ..drawable import Drawable
from ..vector2D import Vector2
from ..frameManager import FRAMES

class PokeInfo(Drawable):
    def __init__(self, pokemon, enemy=False):
        self._enemy = enemy
        self._pokemon = pokemon
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 16)

        if not enemy:
            super().__init__(join("battle", "health_bars.png"), Vector2(130, 72), offset=(0,1))
        else:
            super().__init__(join("battle", "health_bars.png"), Vector2(7, 10), offset=(0,0))
        
        self._blit_name_and_gender()
        

    def _blit_name_and_gender(self):
        start_pos = Vector2(10,7) if self._enemy else Vector2(20,7)
        current_pos = start_pos
        for char in self._pokemon.get_nick_name().lower():
            font_index = int(ord(char)) - 97
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 0))
            font_char.set_colorkey((255,255,255))
            print(font_char)
            self._image.blit(font_char, (current_pos.x, current_pos.y))
            current_pos.x += 5
        
        current_pos.x += 2
        if self._pokemon.get_gender() == "male":
            font_index = 11
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 3))
            self._image.blit(font_char, (current_pos.x, current_pos.y))
        else:
            font_index = 12
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 3))
            self._image.blit(font_char, (current_pos.x, current_pos.y))

        
            