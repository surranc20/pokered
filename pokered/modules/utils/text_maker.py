import pygame
from os.path import join
from ..utils.managers.frameManager import FRAMES


class TextMaker():

    # The font from pokemon fire red is not monospaced so some characters
    # require less space
    SPACES_DICT = {
        join("fonts", "menu_font.png"): {"default": 7},
        join("fonts", "party_txt_font.png"): {
                "default": 5, "Y": 4, "T": 4, "I": 4
            }
    }

    # Sometimes the top left of a font char will be occupied so just getting
    # color at pixel (0,0) will occasionally result in an error
    COLOR_KEYS = {
        join("fonts", "menu_font.png"): (144, 184, 104),
        join("fonts", "party_txt_font.png"): (255, 255, 255)
    }

    def __init__(self, font_name):
        """Creates the text maker which will be able to return text surfaces"""
        self._font_name = font_name

    def get_surface(self, string):
        """Return a surface with the given string displayed as text"""
        text_surface = pygame.Surface(self.calculate_surface_size(string))
        text_surface.fill((255, 255, 254))
        text_surface.set_colorkey((255, 255, 254))
        x_pos = 0
        default_char_len = self.SPACES_DICT[self._font_name]["default"]
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
                x_pos += self.SPACES_DICT[self._font_name].get(
                    str(char), default_char_len)

        return text_surface

    def calculate_surface_size(self, string):
        """Calculates the size to make a surface based on the given string"""
        letter_size = FRAMES.get_frame_size(self._font_name)
        return (letter_size[0] * len(string), letter_size[1])
