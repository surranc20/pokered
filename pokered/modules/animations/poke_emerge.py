from os.path import join
import pygame
from ..frameManager import FRAMES
from ..animated import AnimatedGroupPart
from ..vector2D import Vector2



class PokeEmerge(AnimatedGroupPart):

    PLAYER_POKE_POS = Vector2(78, 112)
    ENEMY_POKE_POS = Vector2(180, 70)
    POKEMON_LOOKUP = {"pikachu" : (6,3)}

    def __init__(self, position, pokemon_name, anim_sequence_pos, thrower = "player"):
        _lookup = self.POKEMON_LOOKUP[pokemon_name]
        _offset = _lookup if thrower != "player" else (_lookup[0] + 1, _lookup[1])
        super().__init__(join("pokemon", "pokemon_big.png"), position, anim_sequence_pos, offset=_offset)
        self._thrower = "player"
        self._frame = 1
        self._orig_image = self._image.copy()
        
        self._anim_started = False
        self._nFrames = 2
        self._animate = True
        self._framesPerSecond = 40

        self._image = self.scale_pokemon()
    
    def __repr__(self):
        return "poke emerge"
    
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
            self._update_position(self._orig_image)
            self.kill()
            return self._orig_image
    
        
        self._anim_started = True
        copy = pygame.transform.scale(self._orig_image, (next_scale_size, next_scale_size))
        self._update_position(copy)
        pygame.transform.threshold(copy, copy, self._image.get_colorkey(), set_color=(244, 189, 244))
        return  copy

        





    




    
        
        
