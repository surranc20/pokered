import pygame
from os.path import join
from ..utils.managers.frameManager import FRAMES


class TextMaker():
    SPACES_DICT = {join("fonts", "menu_font.png"): 6}
    COLOR_KEYS = {join("fonts", "menu_font.png"): (144, 184, 104)}

    def __init__(self, font_name):
        """Creates the text maker which will be able to return text surfaces"""
        self._font_name = font_name

    def get_surface(self, string):
        """Return a surface with the given string displayed as text"""
        text_surface = pygame.Surface(self.calculate_surface_size(string))
        text_surface.fill((255, 255, 254))
        text_surface.set_colorkey((255, 255, 254))
        x_pos = 0
        char_len = FRAMES.get_frame_size(self._font_name)[0]
        for char in string:
            if char.isalpha():
                if char.isupper():
                    ascii_num = 65
                    row = 0
                else:
                    ascii_num = 97
                    row = 1
                font_index = int(ord(char)) - ascii_num
                font_char = FRAMES.getFrame(self._font_name,
                                            offset=(font_index, row))
                font_char.set_colorkey((self.COLOR_KEYS[self._font_name]))
                text_surface.blit(font_char, (x_pos, 0))
                x_pos += char_len
        return text_surface

    def calculate_surface_size(self, string):
        """Calculates the size to make a surface based on the given string"""
        letter_size = FRAMES.get_frame_size(self._font_name)
        return (letter_size[0] * len(string), letter_size[1])
