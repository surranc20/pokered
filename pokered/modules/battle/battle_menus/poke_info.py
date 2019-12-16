import pygame
import math
from os.path import join
from ...utils.drawable import Drawable
from ...utils.vector2D import Vector2
from ...utils.frameManager import FRAMES

class PokeInfo(Drawable):

    ENEMY_POKE_INFO_POS = Vector2(7, 10)
    PLAYER_POKE_INFO_POS = Vector2(130, 72)

    def __init__(self, pokemon, enemy=False, hp=None):
        """This is the info box that appears for each pokemon in battle and contains
        the pokemon's name, hp, level, status, as well as exp status if it is the players pokemon.
        Arguments are a Pokemon and boolean that specifies whether or not this is an info bar of an
        enemies pokemon"""
        self._enemy = enemy
        self._pokemon = pokemon
        self._current_hp = hp

        if not enemy:
            super().__init__(join("battle", "health_bars.png"), self.PLAYER_POKE_INFO_POS, offset=(0,1))
        else:
            super().__init__(join("battle", "health_bars.png"), self.ENEMY_POKE_INFO_POS, offset=(0,0))

        self._blit_name_and_gender()
        self._blit_hp_bar()
        self._blit_lvl()
        self._blit_status()
        if not self._enemy: self._blit_hp_remaining()


    def _blit_name_and_gender(self):
        """Create the name and gender surface."""
        self._text_image = pygame.Surface((self._image.get_width(), self._image.get_height()))
        self._text_image.fill((255,255,255,0))
        self._text_image.set_colorkey((255, 255, 255))
        start_pos = Vector2(10,7) if self._enemy else Vector2(20,7)
        current_pos = start_pos
        for char in self._pokemon.nick_name.lower():
            font_index = int(ord(char)) - 97
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 0))
            font_char.set_colorkey((255,255,255))
            self._text_image.blit(font_char, (current_pos.x, current_pos.y))
            current_pos.x += 5

        current_pos.x += 2
        if self._pokemon.gender == "male":
            font_index = 11
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 3))
            self._text_image.blit(font_char, (current_pos.x, current_pos.y))
        else:
            font_index = 12
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 3))
            self._text_image.blit(font_char, (current_pos.x, current_pos.y))

    def _blit_lvl(self):
        """Create the level surface"""
        self._lvl = pygame.Surface((10, 8))
        self._lvl.fill((255, 255, 255))
        self._lvl.set_colorkey((255,255,255))
        start_pos = Vector2(0, 0)
        current_pos = start_pos
        for char in str(self._pokemon.lvl):
            font_index = int(ord(char)) - 48
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 2))
            font_char.set_colorkey((255,255,255))
            self._lvl.blit(font_char, (current_pos.x, current_pos.y))
            current_pos.x += 5

    def _blit_hp_bar(self):
        """Create the hp bar surface."""
        green = (112, 248, 168)
        yellow = (248, 224, 56)
        red = (241, 14, 14)

        if self._current_hp != None:
            current_hp = self._current_hp
        else: current_hp = self._pokemon.stats["Current HP"]
        max_hp = self._pokemon.stats["HP"]
        percentage = (current_hp / max_hp)

        self._hp = pygame.Surface((math.ceil(percentage * 48), 3))
        if percentage > .50: self._hp.fill(green)
        elif percentage > .15: self._hp.fill(yellow)
        else: self._hp.fill(red)
        self._hp_darken = pygame.Surface((48, 1))
        self._hp_darken.fill((0,0,0))
        self._hp_darken.set_alpha(50)

    def _blit_hp_remaining(self):
        """Create the hp remaining surface."""
        self._hp_remaining = pygame.Surface((35, 8))
        self._hp_remaining.fill((255, 255, 255))
        self._hp_remaining.set_colorkey((255, 255, 255))
        if self._current_hp != None: current_hp = self._current_hp
        else: current_hp = self._pokemon.stats["Current HP"]
        start_pos = Vector2(0,0)
        current_pos = start_pos
        for char in str(str(current_hp) + "/" + str(self._pokemon.stats["HP"])):
            font_index = int(ord(char)) - 48
            font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(font_index, 2))
            if char == "/": font_char = FRAMES.getFrame("pokemon_fire_red_battle_font.png", offset=(4, 3))
            font_char.set_colorkey((255,255,255))
            self._hp_remaining.blit(font_char, (current_pos.x, current_pos.y))
            current_pos.x += 5

    def _blit_status(self):
        """Add the status (ie is it paralyzed) surface."""
        self._status = pygame.Surface((22, 8))
        self._status.fill((255,255,255))
        self._status.set_colorkey((255,255,255))
        for status in self._pokemon.status:
            if status in ["paralyze"]:
                status_char = FRAMES.getFrame("status.png", offset=(1, 0))
                self._status.blit(status_char, (0,0))


    def is_dead(self):
        """Returns whether or not the instance is dead. An instance is dead if its pokemon is dead."""
        return not self._pokemon.is_alive()

    def draw(self, draw_surface):
        """Draws the various subsurfaces to the screen in the correct location based on whether or not the pokemon is an enemy."""
        super().draw(draw_surface)
        draw_surface.blit(self._text_image, (self._position[0], self._position[1]))
        if self._enemy:
            draw_surface.blit(self._hp, (49, 30))
            draw_surface.blit(self._hp_darken, (49, 30))
            draw_surface.blit(self._lvl, (84, 18))
            draw_surface.blit(self._status, (12, 27))

        else:
            draw_surface.blit(self._hp, (181, 91))
            draw_surface.blit(self._hp_darken, (181, 91))
            draw_surface.blit(self._lvl, (217, 79))
            draw_surface.blit(self._hp_remaining, (193, 97))
            draw_surface.blit(self._status, (145, 95))

    def update(self, ticks):
        """Updates the poke info. In reality it just creates another poke info to ensure the current hp
        is always displayed correctly. This can be made more effecient but as of right now it is not a problem."""
        self.__init__(self._pokemon, self._enemy)

