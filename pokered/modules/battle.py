from .vector2D import Vector2
from .drawable import Drawable
from .animated import AnimatedGroup
from .animations.toss_pokemon import TossPokemon
from .battle_menus.poke_info import PokeInfo
from .battle_menus.pokemon_remaining import PokemonRemaining
from .pokemon import Pokemon
from .battle_fsm import BattleFSM
from os.path import join, exists
import pygame

class Battle:
    def __init__(self, player, opponent, draw_surface):
        """Create and show a battle with the player and an npc"""
        self._player = player
        self._opponent = opponent
        self._draw_surface = draw_surface
        self._battle_fsm = BattleFSM(player, opponent, self._draw_surface)
        self._battle_background = Drawable(join("battle", "battle_background.png"), Vector2(0,0), offset= (0,0))
        self._battle_menus = Drawable(join("battle", "battle_menus.png"), Vector2(0,113), offset=(0, 1))
        #self._health_menu_enemy = PokeInfo(Pokemon("pikachu", enemy=True), enemy=True)
        #self._health_menu_player = PokeInfo(Pokemon("caterpie", gender="female"))
        self._toss_anim = TossPokemon("articuno", lead_off=True, enemy=False)
        self._enemy_toss_anim = TossPokemon("pikachu", lead_off=True, enemy=True)
        self._pokemon_remaining = PokemonRemaining(player)
        


        
        pygame.mixer.music.load(join("music", "gym_battle_music.mp3"))
        pygame.mixer.music.play(-1)
    
    def battle_loop(self, game_clock, UPSCALED, screen, running):
        while not self._battle_fsm.is_dead() and running:
            self.draw()
            pygame.transform.scale(self._draw_surface, UPSCALED, screen)
            pygame.display.flip()
            
            game_clock.tick(60)
            for event in pygame.event.get():
                # only do something if the event is of type QUIT or ESCAPE is pressed
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # change the value to False, to exit the main loop
                    running = False
                else: 
                    self._battle_fsm.handle_action(event)
            
            self.update(game_clock.get_time() / 1000)
            
        return running
        
    
    def draw(self):
        for obj in self._battle_fsm.get_draw_list():
            obj.draw(self._draw_surface)

    def update(self, ticks):
        self._battle_fsm.update(ticks)
        for obj in self._battle_fsm.get_update_list():
            new_anim = obj.update(ticks)
            # if new_anim != None: 
            #     self._draw_list.append(new_anim)
            #     if type(new_anim) != Pokemon:
            #         self._update_list.append(new_anim)
                
        




    

