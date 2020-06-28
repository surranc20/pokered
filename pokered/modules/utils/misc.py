def end_at_all(surf, end_coord):
    surf_width = surf.get_width()
    surf_height = surf.get_height()
    start_pos = (end_coord[0] - surf_width, end_coord[1] - surf_height)
    return start_pos


def end_at(surf, end_coord):
    surf_width = surf.get_width()
    start_pos = (end_coord[0] - surf_width, end_coord[1])
    return start_pos

