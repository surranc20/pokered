import pygame
from os.path import join
from ...utils.frameManager import FRAMES
from ...utils.soundManager import SoundManager
from ...utils.drawable import Drawable

class Thunder():
    FRAME_LIST = [[(0, (180, 0))], 
    [(0, (180, 0)), (0, (180, 12), "h")], 
    [(0, (180, 0)), (0, (180, 12), "h"), (1, (180, 0))],
    [(0, (180, 0)), (0, (180, 12), "h"), (1, (180, 0)), (0, (180, 40))],
    [(0, (180, 0)), (0, (180, 12), "h"), (1, (180, 0)), (0, (180, 40)), (1, (180, 8))],
    [(0, (180, 0)), (0, (180, 12), "h"), (2, (180, 0)), (0, (180, 40)), (1, (180, 8))],
    [(0, (180, 0)), (0, (180, 12), "h"), (2, (180, 0)), (0, (180, 40)), (1, (180, 8)), (1, (180, 40))],
    [(2, (180, 0)), (0, (180, 40)), (2, (180, 32)), (1, (180, 40))],
    [(2, (180, -20)), (2, (180, 0)), (2, (180, 32))],
    [(3, (180, -20)), (2, (180, 4)), (2, (180, 36))],
    [(3, (180, -20)), (3, (180, 12)), (2, (180, 36))],
    [(4, (180, -20)), (3, (180, 12)), (3, (180, 34))],
    [(4, (180, -20)), (4, (180, 11)), (3, (180, 34))],
    [(4, (180, -20)), (4, (180, 11)), (4, (180, 34)), (0, (150, 0))],
    [(4, (180, 11)), (4, (180, 34)), (0, (150, 0)), (0, (150, 12), "h")],
    [(4, (180, 34)), (1, (150, 0)), (0, (150, 0)), (0, (150, 12), "h")],
    [(1, (150, 0)), (0, (150, 0)), (0, (150, 12), "h"), (0, (150, 40))], 
    [(1, (150, 0)), (0, (150, 0)), (0, (150, 12), "h"), (0, (150, 40)), (1, (150, 8))],
    [(2, (150, -20)), (0, (150, 12), "h"), (0, (150, 40)), (1, (150, 8))],
    [(2, (150, -20)), (0, (150, 40)), (1, (150, 8)), (1, (150, 40))],
    [(2, (150, -20)), (0, (150, 40)), (2, (150, 12)), (1, (150, 40))],
    [(2, (150, -20)), (2, (150, 12)), (2, (150, 40))], 
    [(2, (150, -20)), (2, (150, 12)), (2, (150, 40)), (0, (200, 0))],
    [(3, (150, -20)), (2, (150, 12)), (2, (150, 40)), (0, (200, 0)), (0, (200, 12), "h")],
    [(3, (150, -20)), (3, (150, 12)), (2, (150, 40)), (0, (200, 0)), (1, (200, 0)), (0, (200, 12), "h")], 
    [(4, (150, -20)), (3, (150, 12)), (2, (150, 40)), (0, (200, 0)), (1, (200, 0)), (0, (200, 12), "h"), (0, (200, 40))], 
    [(4, (150, -20)), (4, (150, 12)), (3, (150, 40)), (2, (200, -20)), (0, (200, 40)), (1, (200, 8)), (1, (200, 40))], 
    [(4, (150, 12)), (4, (150, 40)), (2, (200, -20)), (0, (200, 40)), (2, (200, 8)), (1, (200, 40))], 
    [(4, (150, 40)), (2, (200, -20)), (0, (200, 40)), (2, (200, 8)), (2, (200, 40))], 
    [(4, (150, 40)), (3, (200, -20)), (2, (200, 8)), (2, (200, 40))], 
    [(3, (200, -20)), (2, (200, 8)), (2, (200, 40))], 
    [(4, (200, -20)), (3, (200, 8)), (2, (200, 40))], 
    [(4, (200, -20)), (3, (200, 8)), (3, (200, 40))],
    [(4, (200, 8)), (4, (200, 40))],
    [(4, (200, 40))],
    [], 
    [],
    [],
    [],
    [],
    [],
    [(0, (180, 0))], 
    [(0, (180, 0)), (0, (180, 12), "h")], 
    [(0, (180, 0)), (0, (180, 12), "h"), (1, (180, 0))],
    [(0, (180, 0)), (0, (180, 12), "h"), (1, (180, 0)), (0, (180, 40))],
    [(0, (180, 0)), (0, (180, 12), "h"), (1, (180, 0)), (0, (180, 40)), (1, (180, 8))],
    [(0, (180, 0)), (0, (180, 12), "h"), (2, (180, 0)), (0, (180, 40)), (1, (180, 8))],
    [(0, (180, 0)), (0, (180, 12), "h"), (2, (180, 0)), (0, (180, 40)), (1, (180, 8)), (1, (180, 40))],
    [(2, (180, 0)), (0, (180, 40)), (2, (180, 32)), (1, (180, 40))],
    [(2, (180, -20)), (2, (180, 0)), (2, (180, 32))],
    [(3, (180, -20)), (2, (180, 4)), (2, (180, 36))],
    [(3, (180, -20)), (3, (180, 12)), (2, (180, 36))],
    [(4, (180, -20)), (3, (180, 12)), (3, (180, 34))],
    [(4, (180, -20)), (4, (180, 11)), (3, (180, 34))],
    [(4, (180, -20)), (4, (180, 11)), (4, (180, 34))],
    [(4, (180, 11)), (4, (180, 34))],
    [(4, (180, 34))],
    []]
    def __init__(self, enemy=False):
        self._enemey = enemy
        self._move_file_name = join("moves", "thunder.png")
        self._is_dead = False
        self._move_surface = pygame.Surface((240, 112))
        self._first_frame = FRAMES.getFrame(self._move_file_name, (0,0))
        self._scrolling_background = FRAMES.getFrame(join("moves", "thunder_background.png"))
        self._scrolling_background = FRAMES.reload(join("moves", "thunder_background.png"), (0,0))
        print(self._scrolling_background)

        self._frame_num = 0
        self._fps = 30
        self._animation_timer = 0
        SoundManager.getInstance().playSound(join("moves", "thunder.wav"))

        self._scroll_count = 0 
    
    def is_dead(self):
        return self._is_dead


    def draw(self, draw_surface):
        draw_surface.blit(self._move_surface, (0,0))

    def update(self, ticks):
        self._animation_timer += ticks
        if self._animation_timer > 1 / self._fps:
            self._animation_timer -= 1 / self._fps

            self._scrolling_background.scroll(dx = -1)
            self._move_surface = pygame.Surface((240, 112))
            self._move_surface.set_colorkey((0,0,0))
            frame = self.FRAME_LIST[self._frame_num]
            for sprite in frame:
                sprite_frame = FRAMES.getFrame(self._move_file_name,(sprite[0], 0))
                if len(sprite) == 3:
                    pygame.transform.flip(sprite_frame, True, False)
                
                if self._enemey:
                    self._move_surface.blit(sprite_frame, (sprite[1][0] - 120, max(sprite[1][1], 0) + 40))
                else:
                    self._move_surface.blit(sprite_frame, (sprite[1][0] - 5, sprite[1][1]))
            if self._frame_num < len(self.FRAME_LIST) - 1:
                self._frame_num += 1
            else:
                self._is_dead = True
                self._scrolling_background = FRAMES.reload(join("moves", "thunder_background.png"), (0,0))
                return 

        background_surface = Drawable("", (0,0))
        background_surface._image = pygame.Surface((240, 112))
        background_surface._image.blit(self._scrolling_background, (0,0))
        return background_surface
    



    