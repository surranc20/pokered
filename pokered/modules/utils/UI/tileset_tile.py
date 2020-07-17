from os.path import join
from .drawable import Drawable


class TilesetTile(Drawable):
    def __init__(self, tile_info, pos):
        super().__init__(join("tile sets", tile_info["tileSetName"]), pos, offset=(tile_info["tileColNum"],
                                            tile_info["tileRowNum"]))
