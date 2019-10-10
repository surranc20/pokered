from .vector2D import Vector2
from .drawable import Drawable
from .animated import AnimatedGroup
from .animations.toss_pokemon import TossPokemon
from .pokemon import Pokemon
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
        self._health_menu_enemy = Drawable(join("battle", "health_bars.png"), Vector2(7, 10), offset=(0,0))
        self._health_menu_player = Drawable(join("battle", "health_bars.png"), Vector2(130, 72), offset=(0,1))
        self._toss_anim = TossPokemon("articuno", lead_off=True, enemy=False)
        self._enemy_toss_anim = TossPokemon("pikachu", lead_off=True, enemy=True)
        self._draw_list = [self._battle_background, self._battle_menus, self._toss_anim, self._enemy_toss_anim, self._health_menu_enemy, self._health_menu_player]
        self._update_list = [self._toss_anim, self._enemy_toss_anim]

        self._finished = False
        pygame.mixer.music.load(join("music", "gym_battle_music.mp3"))
        pygame.mixer.music.play(-1)
    
    def battle_loop(self, game_clock, UPSCALED, screen, running):
        while not self._finished and running:
            self.draw()
            pygame.transform.scale(self._draw_surface, UPSCALED, screen)
            pygame.display.flip()
            
            game_clock.tick(60)
            for event in pygame.event.get():
                # only do something if the event is of type QUIT or ESCAPE is pressed
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # change the value to False, to exit the main loop
                    running = False
            
            self.update(game_clock.get_time() / 1000)
            self._update_list = [obj for obj in self._update_list if not obj.is_dead()]
            self._draw_list = [obj for obj in self._draw_list if not obj.is_dead()]
        return running
        
    
    def draw(self):
        for obj in self._draw_list:
            obj.draw(self._draw_surface)

    def update(self, ticks):
        for obj in self._update_list:
            new_anim = obj.update(ticks)
            if new_anim != None: 
                self._draw_list.append(new_anim)
                if type(new_anim) != Pokemon:
                    self._update_list.append(new_anim)
                
        




    

