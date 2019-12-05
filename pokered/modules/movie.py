import pygame
from os.path import join
from .utils.soundManager import SoundManager
from .enumerated.battle_actions import BattleActions

class Movie():
    def __init__(self, screen_size, folder_name):
        self._surface = pygame.Surface(screen_size)
        self._folder_name = folder_name
        self._counter = 0
        self._timer = 0
        self._fps = 20
        self._is_over = False
        self._frame = pygame.image.load(join(self._folder_name, "scene00001.png"))
        self._frame.convert()
        self._surface.blit(self._frame, (0,0))
        SoundManager.getInstance().playMusic("intro.mp3")
    
    def draw(self, draw_surface):
        draw_surface.blit(self._surface, (0,0))

    def update(self, ticks):
        self._timer += ticks
        if self._timer > 1 / self._fps:
            self._counter += 1
            try:
                self._frame = pygame.image.load(join(self._folder_name, "scene" + self._get_num() + ".png"))
                self._frame.convert()
            except:
                self._counter =1
                self._frame = pygame.image.load(join(self._folder_name, "scene" + self._get_num() + ".png"))
                self._frame.convert()
                SoundManager.getInstance().playMusic("intro.mp3")
            self._surface.blit(self._frame, (0,0))
            self._timer -= 1 /self._fps

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            self._is_over = True

    def is_over(self):
        return self._is_over
    
    def get_end_event(self):
        return "INTRO OVER"

    def _get_num(self):
        print(str(self._counter).zfill(5))
        return str(self._counter).zfill(5)

    
