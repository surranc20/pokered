import pygame
import textwrap
from os.path import join
from ..enumerated.battle_actions import BattleActions
from ..utils.managers.soundManager import SoundManager



class WhiteOut():
    def __init__(self, player):
        """Creates a white out event. This is the screen that plays when the player loses. Right now
        it will restart the game when the player presses enter."""
        self._player = player
        self._white_out_surface = pygame.Surface((240, 160))
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 15)
        self._blit_line()
        self._is_over = False

    def draw(self, draw_surface):
        """Draws the event"""
        draw_surface.blit(self._white_out_surface, (0, 0))


    def update(self, ticks):
        """This event does not need to do anything in update."""
        pass

    def handle_event(self, event):
        """If the player presses enter the event is ended."""
        if event.type == pygame.KEYDOWN and event.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            self._is_over = True

    def is_over(self):
        """Returns whether or not the event is over."""
        return self._is_over

    def get_end_event(self):
        """Tells the level manager to tell the game manager to restart the game."""
        return "RESTART"

    def _blit_line(self):
        """Blits the text that displays to the white out surface."""
        string = "Your were defeated by the Elite Four! Thanks for playing the demo of POKeRED. Press enter to restart the game!"
        self._white_out_surface.fill((0, 0, 0))
        string_lyst = textwrap.wrap(string, width=41)
        height = 50
        for string in string_lyst:
            rendered = self._font.render(string, False, (255,255,255))
            self._white_out_surface.blit(rendered, (20, height))
            height += 15
