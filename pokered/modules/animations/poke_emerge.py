from os.path import join
import pygame
from ..frameManager import FRAMES
from ..animated import AnimatedGroupPart
from ..vector2D import Vector2



class PokeEmerge(AnimatedGroupPart):

    PLAYER_POKE_POS = Vector2(78, 105)
    ENEMY_POKE_POS = Vector2(180, 70)

    def __init__(self, position, pokemon_name, anim_sequence_pos, thrower = "player"):
        super().__init__(join("pokemon", pokemon_name + "~.png"), position, anim_sequence_pos)
        self._thrower = "player"
        self._frame = 1
        self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
        self._orig_image = self._image.copy()
        
        self._anim_started = False
        self._nFrames = 2
        self._animate = True
        self._framesPerSecond = 1

        self._image = self.scale_pokemon()
    
    def update(self, ticks):
        if self._animate:
            self._animationTimer += ticks

        if self._animationTimer > 1 / self._framesPerSecond:
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = self.scale_pokemon()
            
    def _update_position(self, copy):
        if self._thrower == "player": pos = self.PLAYER_POKE_POS
        else: pos = self.ENEMY_POKE_POS

        self._position.x = pos.x  - copy.get_width() // 2
        self._position.y = pos.y - copy.get_height()
        print(self._position.y + copy.get_height())



    def scale_pokemon(self):
        if not self._anim_started:
            next_scale_size = 8
        else:
            next_scale_size = self._image.get_height() + 8

        if next_scale_size >= 64 and self._anim_started: 
            #self.kill()
            return self._orig_image
    
        
        self._anim_started = True
        copy = pygame.transform.scale(self._orig_image, (next_scale_size, next_scale_size))
        self._update_position(copy)
        pygame.transform.threshold(copy, copy, self._image.get_colorkey(), set_color=(244, 189, 244))
        return  copy

        





    




    
        
        
