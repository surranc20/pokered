from os.path import join
from .managers.frameManager import FRAMES
from .text_maker import TextMaker


def end_at_all(surf, end_coord):
    """Returns the coordinate a surface needs to start at to end at the end
    coordinate."""
    surf_width = surf.get_width()
    surf_height = surf.get_height()
    start_pos = (end_coord[0] - surf_width, end_coord[1] - surf_height)
    return start_pos


def end_at(surf, end_coord):
    """Returns the coordinate something needs to start at to end at the end
    coordinate. Does not care about y dimension"""
    surf_width = surf.get_width()
    start_pos = (end_coord[0] - surf_width, end_coord[1])
    return start_pos


def center(surf, start_x, end_x, y):
    """Returns the coordinate something needs to start at to be centered
    between two x coordinates."""
    width = end_x - start_x
    return (((width - surf.get_width()) // 2) + start_x, y)


def create_desc_surf(item):
    """Creates the desacription surface for the given item"""
    text_maker = TextMaker(join("fonts", "menu_font.png"), 200)
    try:
        description = item.description
        return text_maker.get_surface(description)

    except AttributeError:
        return text_maker.get_surface("CLOSE BAG")


def create_pic_surf(item):
    """Creates the picture description for the given item"""
    try:
        return item.item_surf

    except AttributeError:
        return FRAMES.getFrame("back_arrow.png")
