import pygame
from os.path import join, exists

from ..utils.vector2D import Vector2
from ..utils.drawable import Drawable
from ..utils.animated import AnimatedGroup
from ..animations.toss_pokemon import TossPokemon
from ..pokemon import Pokemon
from .battle_menus.poke_info import PokeInfo
from .battle_menus.pokemon_remaining import PokemonRemaining
from .battle_fsm import BattleFSM



class Battle:
    def __init__(self, player, opponent):
        """Create and show a battle with the player and an npc"""
        self._player = player
        self._opponent = opponent
        self._battle_fsm = BattleFSM(player, opponent)
        self._battle_background = Drawable(join("battle", "battle_background.png"), Vector2(0,0), offset= (0,0))
        self._battle_menus = Drawable(join("battle", "battle_menus.png"), Vector2(0,113), offset=(0, 1))
        self._toss_anim = TossPokemon("articuno", lead_off=True, enemy=False)
        self._enemy_toss_anim = TossPokemon("pikachu", lead_off=True, enemy=True)
        self._pokemon_remaining = PokemonRemaining(player)
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
            new_anim = obj.update(ticks)
            
                
        




    

