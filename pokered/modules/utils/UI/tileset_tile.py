from os.path import join
from .drawable import Drawable


class TilesetTile(Drawable):
    FOREGROUND_LINK = {
        "tileset_66.png": {
            (0, 0): (0, 0),
            (1, 0): (1, 0),
            (1, 32): (2, 0),
            (2, 32): (3, 0),
            (0, 10): (4, 0)
        },
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
            self.FOREGROUND_LINK[self.tile_info["tileSetName"]].get(self.offset)

        if offset is None:
            return None
        else:
            return Drawable(tile_file_name, self.pos, offset=offset)
