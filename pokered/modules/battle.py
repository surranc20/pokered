from .vector2D import Vector2
from .drawable import Drawable
from .animations.trainer_toss import TrainerToss
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
        self._toss_anim = TrainerToss(Vector2(0, 0))
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
        return running
        
    
    def draw(self):
        self._battle_background.draw(self._draw_surface)
        self._battle_menus.draw(self._draw_surface)
        self._toss_anim.draw(self._draw_surface)

    def update(self, ticks):
        self._toss_anim.update(ticks)




    

