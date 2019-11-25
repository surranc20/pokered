import pygame
from os.path import join, exists

from ..utils.vector2D import Vector2
from ..utils.drawable import Drawable
from ..utils.animated import AnimatedGroup
from ..animations.toss_pokemon import TossPokemon
from ..animations.moves.scrolling_move import ScrollingMove
from ..pokemon import Pokemon
from .battle_menus.poke_info import PokeInfo
from .battle_menus.pokemon_remaining import PokemonRemaining
from .battle_fsm import BattleFSM



class Battle:
    def __init__(self, player, opponent):
        """Create and show a battle with the player and an npc"""
        Drawable.WINDOW_OFFSET = Vector2(0,0)
        self._player = player
        self._opponent = opponent
        self._battle_fsm = BattleFSM(player, opponent)
        pygame.mixer.music.load(join("music", "gym_battle_music.mp3"))
        pygame.mixer.music.play(-1)
    
    def handle_event(self, event):
        self._battle_fsm.handle_action(event)
    
    def draw(self, draw_surface):
        for obj in self._battle_fsm.get_draw_list():
            if obj != None:
                obj.draw(draw_surface)

    def update(self, ticks):
        self._battle_fsm.update(ticks)
        for obj in self._battle_fsm.get_update_list():
            if issubclass(type(obj), ScrollingMove):
                background = obj.update(ticks)
                self._battle_fsm._scrolling_background_surf = background
                
            else:
                new_anim = obj.update(ticks)
    
    def is_over(self):
        if self._battle_fsm.is_over():
            pygame.mixer.music.pause()
        return self._battle_fsm.is_over()

            
                
        




    

