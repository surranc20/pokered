from os.path import join
from .animated import Animated


class TilesetAnimatedTile(Animated):
    DOOR_FILE_LINK = {
        "tileset_66.png": {
            (3, 10): ["elite_four_door.png", 1, 2],
            (3, 9): ["elite_four_door.png", 0, 2],
            (3, 11): ["elite_four_entry_door.png", 0, 2],
            (3, 12): ["elite_four_entry_door.png", 1, 2],
            (2, 11): ["elite_four_entry_door_left.png", 0, 2],
            (2, 12): ["elite_four_entry_door_left.png", 1, 2],
            (4, 11): ["elite_four_entry_door_right.png", 0, 2],
            (4, 12): ["elite_four_entry_door_right.png", 1, 2],
        }
    }

    def __init__(self, tile_info, pos):
        tile_pos = (tile_info["columnNum"], tile_info["rowNum"])
        tile_file_name, self.offset, num_frames = \
            self.DOOR_FILE_LINK[tile_info["tileSetName"]][tile_pos]

        self.tile_file_name = join("doors", tile_file_name)
        self.tile_info = tile_info
        self.pos = pos

        super().__init__(self.tile_file_name, pos, offset=(0, self.offset))
        self._nFrames = num_frames
        self._framesPerSecond = 1

    def create_foreground(self):
        tile_file_name = f"{self.tile_file_name[:-4]}_transparent.png"
        tile = Animated(tile_file_name, self.pos, offset=(0, self.offset))
        tile._nFrames = self._nFrames
        tile._framesPerSecond = self._framesPerSecond
        return tile

