import pygame
from os.path import join
from ..utils.managers.frameManager import FRAMES


class TextMaker():

    # The font from pokemon fire red is not monospaced so some characters
    # require less space
    SPACES_DICT = {
        join("fonts", "menu_font.png"): {
            "default": 7, "l": 4, "i": 3, "n": 6, "r": 6
            },
        join("fonts", "party_txt_font.png"): {
                "default": 5, "Y": 4, "T": 4, "I": 4, "1": 4
            }
    }

    # Sometimes the top left of a font char will be occupied so just getting
    # color at pixel (0,0) will occasionally result in an error
    COLOR_KEYS = {
        join("fonts", "menu_font.png"): (144, 184, 104),
        join("fonts", "party_txt_font.png"): (255, 255, 255)
    }

    # { is a symbol for boy logo and } is a symbol for girl logo
    LOCATION = {
        join("fonts", "party_txt_font.png"): {".": (0, 26), "{": (3, 11),
                                              "}": (3, 12), "/": (3, 4),
                                              "é": (3, 13), "!": (3, 0),
                                              "~": (3, 14), "?": (3, 1)},
        join("fonts", "menu_font.png"): {".": (3, 6), "/": (3, 4),
                                         "é": (3, 7)}
    }

    def __init__(self, font_name, max=None, line_height=None):
        """Creates the text maker which will be able to return text surfaces"""
        self._font_name = font_name
        self._max = max
        self.line_height = line_height if line_height is not None else \
            FRAMES.get_frame_size(self._font_name)[1] + 2

    def get_surface(self, string):
        """Return a surface with the given string displayed as text"""
        text_surface = pygame.Surface(self.calculate_surface_size(string))
        text_surface.fill((255, 255, 254))
        text_surface.set_colorkey((255, 255, 254))
        x_pos = 0
        y_pos = 0
        default_char_len = self.SPACES_DICT[self._font_name]["default"]
        for word in string.split():
            if self._max is not None:
                if len(word) * default_char_len + x_pos > self._max:
                    y_pos += self.line_height
                    x_pos = 0
            for char in word:
                if char in [".", "{", "}", "/", "é", "!", "~", "?"]:
                    if char == "é" and \
                            self._font_name == join("fonts",
                                                    "party_txt_font.png"):
                        y_offset = -1
                    else:
                        y_offset = 0

                    row, font_index = self.LOCATION[self._font_name][char]

                    font_char = FRAMES.getFrame(self._font_name,
                                                offset=(font_index, row))
                    font_char.set_colorkey((self.COLOR_KEYS[self._font_name]))
                    text_surface.blit(font_char, (x_pos, y_pos + y_offset))
                    x_pos += self.SPACES_DICT[self._font_name].get(
                        str(char), default_char_len)

                elif char.isalnum():
                    if char.isupper():
                        ascii_num = 65
                        row = 0
                    elif char.islower():
                        ascii_num = 97
                        row = 1
                    else:
                        ascii_num = 48
                        row = 2
                    font_index = int(ord(char)) - ascii_num
                    font_char = FRAMES.getFrame(self._font_name,
                                                offset=(font_index, row))
                    font_char.set_colorkey((self.COLOR_KEYS[self._font_name]))
                    text_surface.blit(font_char, (x_pos, y_pos))
                    x_pos += self.SPACES_DICT[self._font_name].get(
                        str(char), default_char_len)

            x_pos += 4
            self.pos = (x_pos, y_pos)

        return text_surface

    def calculate_surface_size(self, string):
        """Calculates the size to make a surface based on the given string"""
        letter_size = int(self.SPACES_DICT[self._font_name]["default"])
        x_size = letter_size * len(string)
        y_size = self.line_height
        if self._max is not None:
            while x_size > self._max:
                x_size -= self._max
                y_size += self.line_height

        return (letter_size * len(string), y_size)
