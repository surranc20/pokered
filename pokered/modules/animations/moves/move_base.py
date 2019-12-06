import pygame
from os.path import join
from ...utils.frameManager import FRAMES
from ...utils.drawable import Drawable


class MoveBase():
    """Generic move class that all other moves are based on. Takes the attacking and defending
    pokemon as inputs as well as a boolean value representing whether or not the enemy is the pokemon
    that is the attacking pokemon."""
    def __init__(self, attacker, defender, enemy=False):
        self._attacker = attacker
        self._defender = defender
        self._enemy = enemy
        self._is_dead = False
        
        # Create the move surface that all move animations will be blitted to
        self._move_surface = pygame.Surface((240, 112))
        self._move_surface.set_colorkey((0,0,0))

        # Set the current frame being displayed by the MoveBase
        self._frame_num = 0

        # Controls how many frames the MoveBase will display per second
        self._fps = 30
        self._animation_timer = 0

    def is_dead(self):
        """Returns whether or not the MoveBase has finished its current animation."""
        return self._is_dead
    
    def draw(self, draw_surface):
        """Draw the current frame"""
        draw_surface.blit(self._move_surface, (0,0))
    
    def update(self, ticks):
        """Handles the updating of the MoveBase. Changes current frame at a speed
        depending on the set fps. When the frame changes the new frame is blitted to the move surface."""
        self._animation_timer += ticks
        if self._animation_timer > 1 / self._fps:
            self._animation_timer -= 1 / self._fps

            # Creates a new move surface which effectively erases the last frame
            self._move_surface = pygame.Surface((240, 112))
            self._move_surface.set_colorkey((0,0,0))

            # Read the frame from the frame list
            frame = self.FRAME_LIST[self._frame_num]

            # Each frame can consist of more than one sprite
            # A frame is in the following form. [(offset in given sprite sheet, (x pos, y pos))]
            for sprite in frame:
                sprite_frame = FRAMES.getFrame(self._move_file_name,(sprite[0], 0))

                # If the sprite has a third argument is specefies a rotation of the given frame
                if len(sprite) == 3:

                    # Flip horizontal
                    if sprite[2] == "h":
                        sprite_frame = pygame.transform.flip(sprite_frame, True, False)
                    
                    # Flip vertical
                    elif sprite[2] == "v":
                        sprite_frame = pygame.transform.flip(sprite_frame, False, True)
                    
                    # Flip horizontally and vertically
                    elif sprite[2] == "hv":
                        sprite_frame = pygame.transform.flip(sprite_frame, True, True)
                    
                    # Rotate 90 degrees
                    elif sprite[2] == "r":
                        sprite_frame = pygame.transform.rotate(sprite_frame, 90)
                
                # In order to make enemy moves appear correctly we must change add an offset to the x and y pos specified in the frame
                if self._enemy:
                    self._move_surface.blit(sprite_frame, (sprite[1][0] - 120, max(sprite[1][1], 0) + 40))
                else:
                    self._move_surface.blit(sprite_frame, (sprite[1][0] - 5, sprite[1][1]))
            
            # Go to next frame or end animation
            if self._frame_num < len(self.FRAME_LIST) - 1:
                self._frame_num += 1
            else:
                 self._is_dead = True
                 

        
        

