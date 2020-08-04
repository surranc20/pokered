from os.path import join
from .animated import Animated


class TilesetAnimatedTile(Animated):
    DOOR_FILE_LINK = {
        "tileset_66.png": {
            (3, 10): ["elite_four_door.png", 1, 2],
            (3, 9): ["elite_four_door.png", 0, 2]
        }
    }

    def __init__(self, tile_info, pos):
        tile_pos = (tile_info["columnNum"], tile_info["rowNum"])
        tile_file_name, offset, num_frames = \
            self.DOOR_FILE_LINK[tile_info["tileSetName"]][tile_pos]

        tile_file_name = join("doors", tile_file_name)
        self.tile_info = tile_info

        # FIND
        super().__init__(tile_file_name, pos, offset=(0, offset))
        self._nFrames = num_frames
        self._framesPerSecond = 1
