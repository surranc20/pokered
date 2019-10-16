import pygame
from os.path import join
from ..drawable import Drawable
from ..vector2D import Vector2
from ..frameManager import FRAMES

class PokeInfo(Drawable):

    ENEMY_POKE_INFO_POS = Vector2(7, 10)
    PLAYER_POKE_INFO_POS = Vector2(130, 72)

    def __init__(self, pokemon, enemy=False):
        """This is the info box that appears for each pokemon in battle and contains
        the pokemon's name, hp, level, status, as well as exp status if it is the players pokemon.
        Arguments are a Pokemon and boolean that specifies whether or not this is an info bar of an 
        enemies pokemon"""
        self._enemy = enemy
        self._pokemon = pokemon

        if not enemy:
            super().__init__(join("battle", "health_bars.png"), self.PLAYER_POKE_INFO_POS, offset=(0,1))
        else:
            super().__init__(join("battle", "health_bars.png"), self.ENEMY_POKE_INFO_POS, offset=(0,0))
        
        self._blit_name_and_gender()
        

    def _blit_name_and_gender(self):
        #TODO: This way of accomplishing this has serious negative side effects.
        #TODO: Clean up some of the magic numbers here
        start_pos = Vector2(10,7) if self._enemy else Vector2(20,7)
        current_pos = start_pos
        for char in self._pokemon.get_nick_name().lower():
            print(char)
            font_index = int(ord(char)) - 97
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 0))
            font_char.set_colorkey((255,255,255))
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

    def is_dead(self):
        """Returns whether or not the instance is dead. 
        An instance is dead if its pokemon is dead."""
        return not self._pokemon.is_alive()