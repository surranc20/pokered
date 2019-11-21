import pygame
import json
import random
from os.path import join
from ..utils.frameManager import FRAMES
from ..utils.soundManager import SoundManager
from ..utils.animated import AnimatedGroupPart
from ..utils.vector2D import Vector2



class PokeEmerge(AnimatedGroupPart):

    # Locations on battle_map where pokemon emerge. 
    # Pokemon will be centered width wise on this location
    # and will terminate height wise on this location.
    PLAYER_POKE_POS = Vector2(68, 112)
    ENEMY_POKE_POS = Vector2(180, 70)

    def __init__(self, position, pokemon_name, anim_sequence_pos, enemy = False):
        """This is animation that plays when a pokemon is emerging from a pokeball. Has all the 
        same arguments as an AnimatedGroupPart as well as an enemy argument which is necessary 
        becuase it tells PokeEmerge whether or not to use the front or back of the pokemon and 
        where to draw the animation when it is occuring."""

        # Look up pokemon position in sprite sheet and determine whether or not to use the 
        # front or back image of the pokemon
        with open(join("jsons", "pokemon_lookup.json"), "r") as pokemon_lookup_json:
            pokemon_lookup = json.load(pokemon_lookup_json)
            _lookup = tuple(pokemon_lookup[pokemon_name])
        _offset = _lookup if enemy else (_lookup[0] + 1, _lookup[1])
        super().__init__(join("pokemon", "pokemon_big.png"), position, anim_sequence_pos, offset=_offset)

        self._pokemon_name = pokemon_name
        self._enemy = enemy
        self._frame = 1
        self._orig_image = self._image.copy()
        
        self._anim_started = False
        self._nFrames = 2
        self._animate = True
        self._framesPerSecond = 30

        # Initial image for PokeEmerge needs to be the smallest version of the pokemon
        self._image = self.scale_pokemon()
    
    def __repr__(self):
        """Returns the representation of PokeEmerge. Simply 'Poke Emerge'. 
        Used primarily for debugging."""
        return "Poke Emerge"
    
    def update(self, ticks):
        """Overrides the update of AnimatedGroupPart. Decides whether the pokemon should be
        scaled up to the next size based on the animation timer"""
        if self._animate:
            self._animationTimer += ticks

        if self._animationTimer > 1 / self._framesPerSecond:
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = self.scale_pokemon()
            
    def _update_position(self, image):
        """Helper method used to update the position of the image after it has been scalled. 
        This is necessary because scaling changes the dimensions of the image and the image needs
        to be centered on the position specified in PLAYER_POKE_POS of ENEMY_POKE_POS."""
        if not self._enemy: pos = self.PLAYER_POKE_POS
        else: pos = self.ENEMY_POKE_POS

        self._position.x = pos.x  - image.get_width() // 2
        self._position.y = pos.y - image.get_height()

    def scale_pokemon(self):
        """Calculates the next valid size for the pokemon and then scales to that
        size. Also makes the pokemon image purple. Returns the new scaled image 
        after scaling operation is complete."""

        if not self._anim_started: 
            next_scale_size = 8
            self._anim_started = True
        else: next_scale_size = self._image.get_height() + 8

        # If the next_scale_size is > 64 then the animation is done.
        if next_scale_size >= 64: 
            self._update_position(self._orig_image)
            self.kill()
            if self._pokemon_name.capitalize() == "Pikachu":
                rando = str(random.randint(1,97))
                print(rando)
                SoundManager.getInstance().playSound(join("cries", self._pokemon_name.capitalize(), "025 - Pikachu (" + rando + ").wav"))
            else: SoundManager.getInstance().playSound(join("cries", self._pokemon_name.capitalize() + ".wav"))
            return self._orig_image

        # Scale pokemon and then update its position
        copy = pygame.transform.scale(self._orig_image, (next_scale_size, next_scale_size))
        self._update_position(copy)

        # Turn all non-transparent pixels purple
        pygame.transform.threshold(copy, copy, self._image.get_colorkey(), set_color=(244, 189, 244))
        return  copy

        





    




    
        
        
