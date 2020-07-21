from os.path import join
from .drawable import Drawable


class TilesetTile(Drawable):
    def __init__(self, tile_info, pos):
        print(tile_info)
        super().__init__(join("tile sets", tile_info["tileSetName"]), pos, offset=(tile_info["columnNum"],
                                            tile_info["rowNum"]))
