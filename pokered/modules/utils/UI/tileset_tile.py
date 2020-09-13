from os.path import join
from .drawable import Drawable


class TilesetTile(Drawable):
    FOREGROUND_LINK = {
        "tileset_66.png": {
            (0, 0): (0, 0),
            (1, 0): (1, 0),
            (1, 32): (2, 0),
            (2, 32): (3, 0),
            (0, 10): (4, 0),
            (1, 34): (5, 0),
            (0, 34): (6, 0),
            (1, 36): (7, 0),
            (0, 36): (0, 1),
            (0, 37): (1, 1),
            (1, 37): (2, 1),
            (2, 37): (3, 1),
            (3, 37): (4, 1)
        },
        "tileset_14.png": {
            (0, 24): (0, 0),
            (3, 36): (1, 0),
            (0, 10): (2, 0),
            (1, 18): (3, 0),
            (0, 18): (4, 0),
            (0, 9): (5, 0),
            (0, 32): (6, 0),
        },
        "tileset_12.png": {},
        "black.png": {}
    }

    def __init__(self, tile_info, pos, tile_type="background"):

        tile_file_name = join("tile sets", tile_info["tileSetName"])
        offset = (tile_info["columnNum"], tile_info["rowNum"])

        self.offset = offset
        self.tile_info = tile_info
        self.tile_file_name = tile_file_name
        self.pos = pos
        super().__init__(tile_file_name, pos, offset=offset)

    def create_foreground(self):
        tile_file_name = f"{self.tile_file_name[:-4]}_transparent.png"
        offset = \
            self.FOREGROUND_LINK[self.tile_info["tileSetName"]].get(self.offset)  # NOQA

        if offset is None:
            return None
        else:
            return Drawable(tile_file_name, self.pos, offset=offset)
