import pygame
from os.path import join

from .text_maker import TextMaker


def end_at_all(surf, end_coord):
    surf_width = surf.get_width()
    surf_height = surf.get_height()
    start_pos = (end_coord[0] - surf_width, end_coord[1] - surf_height)
    return start_pos


def end_at(surf, end_coord):
    surf_width = surf.get_width()
    start_pos = (end_coord[0] - surf_width, end_coord[1])
    return start_pos


def create_desc_surf(item):
    """Creates the desacription surface for the given item"""
    try:
        description = item.description
        text_maker = TextMaker(join("fonts", "menu_font.png"), 200)
        return text_maker.get_surface(description)

    except AttributeError:
        return pygame.Surface((0, 0))
