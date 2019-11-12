import json
from os.path import join
from .utils.drawable import Drawable

class Level():
    TILE_SIZE = 16
    def __init__(self, level_name, player, screen_size):
        self._player = player
        self._screen_size = screen_size
        self._foreground = Drawable(join(level_name, "level_foreground.png"),(0,0))
        self._background = Drawable(join(level_name, "level_background.png"), (0,0))
        with open(join("levels", level_name,"meta.json"), "r") as level_json:
            level_meta = json.load(level_json)
            self._level_size = (self.TILE_SIZE * level_meta[0][0], self.TILE_SIZE * level_meta[0][1])
            self._colide_list = level_meta[1]
            print(self._level_size)
        self._tiles = self._tile()
        self._foreground.center_with_border(screen_size)
        self._background.center_with_border(screen_size)

        
    
    def _tile(self):
        tile_dims = (self._level_size[0] // self.TILE_SIZE, self._level_size[1] // self.TILE_SIZE)
        print(tile_dims)

        tiles = []
        for y in range(tile_dims[1]):
            row = []
            for x in range(tile_dims[0]):
                row.append(Tile((x,y), self._colide_list[y][x], None))
            tiles.append(row)
        
        for row in tiles:
            print(row)


    def draw(self, draw_surface):
        self._background.draw(draw_surface)
        self._player.draw(draw_surface)
        self._foreground.draw(draw_surface)
    
    def update(self, ticks):
        self._player.update(ticks)
        Drawable.updateWindowOffset(self._player, self._screen_size, self._level_size)

class Tile:
    def __init__(self, pos, colidable, contains):
        self._pos = pos
        self._contains = contains
        self._colidable = True if colidable == 1 else False
    
    def __repr__(self):
        return str(self._colidable)