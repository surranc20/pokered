from .vector2D import Vector2
from .drawable import Drawable
import pygame

class Battle:
    def __init__(self, player, opponent, draw_surface):
        """Create and show a battle with the player and an npc"""
        self._player = player
        self._opponent = opponent
        self._draw_surface = draw_surface
        self._battle_background = Drawable("battle_background.png", Vector2(0,0))
        
    
    def draw(self):
        self._battle_background.draw(self._draw_surface)




    

