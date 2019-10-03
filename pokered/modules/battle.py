from .vector2D import Vector2
from .drawable import Drawable
from os.path import join
import pygame

class Battle:
    def __init__(self, player, opponent, draw_surface):
        """Create and show a battle with the player and an npc"""
        self._player = player
        self._opponent = opponent
        self._draw_surface = draw_surface
        self._battle_background = Drawable(join("battle", "battle_background.png"), Vector2(0,0), offset= (0,0))
        self._battle_menus = Drawable(join("battle", "battle_menus.png"), Vector2(0,113), offset=(0, 1))
        pygame.mixer.music.load(join("music", "gym_battle_music.mp3"))
        pygame.mixer.music.play(-1)
        
    
    def draw(self):
        self._battle_background.draw(self._draw_surface)
        self._battle_menus.draw(self._draw_surface)




    

