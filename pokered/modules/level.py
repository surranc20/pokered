import json
import pygame
from os.path import join
from .trainer import Trainer
from .pokemon import Pokemon
from .utils.drawable import Drawable
from .utils.vector2D import Vector2
from .utils.soundManager import SoundManager
from .enumerated.cardinality import Cardinality

class Level():
    TILE_SIZE = 16
    def __init__(self, level_name, player, screen_size):
        self._player = player
        self._screen_size = screen_size
        self._foreground = Drawable(join(level_name, "level_foreground.png"),(0,0))
        self._background = Drawable(join(level_name, "level_background.png"), (0,0))
        with open(join("levels", level_name,"meta.json"), "r") as level_json:
            self._level_meta = json.load(level_json)
            self._level_size = (self.TILE_SIZE * self._level_meta[0][0], self.TILE_SIZE * self._level_meta[0][1])
            self._colide_list = self._level_meta[3]
        self._tiles = self._tile()
        self._foreground.center_with_border(screen_size)
        self._background.center_with_border(screen_size)
        self.populate_trainers()
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)

        
    
    def _tile(self):
        tile_dims = (self._level_size[0] // self.TILE_SIZE, self._level_size[1] // self.TILE_SIZE)
        tiles = []
        for y in range(tile_dims[1]):
            row = []
            for x in range(tile_dims[0]):
                row.append(Tile((x,y), self._colide_list[y][x], None))
            tiles.append(row)
        for row in tiles:
            print(row)
        return tiles
    
    def populate_trainers(self):
        self._player.setPosition(self.correct_border_and_height_pos(self._level_meta[1]))
        self._tiles[self._level_meta[1][1]][self._level_meta[1][0]].add_obj(self._player)
        for trainer_args in self._level_meta[2]:
            train = Trainer(self.correct_border_and_height_pos(trainer_args[0]), trainer_args[1], trainer_args[2], enemy=True)
            for pokemon in trainer_args[3]:
                print(pokemon)
                train._pokemon_team.append(Pokemon(pokemon, enemy=True))
            print("pos", train._position)
            self._tiles[trainer_args[0][1]][trainer_args[0][0]].add_obj(train)


    def draw(self, draw_surface):
        self._background.draw(draw_surface)
        for row in self._tiles:
            for tile in row:
                tile.draw(draw_surface)
        self._foreground.draw(draw_surface)
    
    def update(self, ticks):
        for y, row in enumerate(self._tiles):
            for x, tile in enumerate(row):
                tile.update(ticks, self.get_nearby_tiles((x,y)))
        Drawable.updateWindowOffset(self._player, self._screen_size, self._level_size)
    
    def get_nearby_tiles(self, pos):
        nearby_tiles = {}
        if self.tile_within_map((pos[0], pos[1] - 1)):
            nearby_tiles[Cardinality.NORTH] = self._tiles[pos[1] - 1][pos[0]]
        if self.tile_within_map((pos[0], pos[1] + 1)):
            nearby_tiles[Cardinality.SOUTH] = self._tiles[pos[1] + 1][pos[0]]
        if self.tile_within_map((pos[0] - 1, pos[1])):
            nearby_tiles[Cardinality.WEST] = self._tiles[pos[1]][pos[0] - 1]
        if self.tile_within_map((pos[0] + 1, pos[1])):
            nearby_tiles[Cardinality.EAST] = self._tiles[pos[1]][pos[0] + 1]
        
        return nearby_tiles

    def tile_within_map(self, pos):
        tile_dims = (self._level_size[0] // self.TILE_SIZE, self._level_size[1] // self.TILE_SIZE)
        if pos[0] < 0 or pos[1] < 0: return False
        elif pos[0] >= tile_dims[0] or pos[1] >= tile_dims[1]: return False
        else: return True
    
    def correct_border_and_height_pos(self, pos):
        return Vector2(pos[0] * self.TILE_SIZE + self._foreground._x_off, pos[1] * self.TILE_SIZE - 6)


class Tile:
    def __init__(self, pos, colidable, obj):
        self._pos = pos
        self._obj = obj
        self._base_colidable = colidable
        self._colidable = True if colidable == 1 else False
    
    def add_obj(self, obj):
        if self._obj == None:
            self._obj = obj
            self._colidable = True
        else:
            raise Exception
    
    def remove_obj(self):
        self._obj = None
        self._colidable = self._base_colidable
    
    def is_clear(self):
        return not self._colidable
    
    def draw(self, draw_surface):
        if self._obj != None:
            self._obj.draw(draw_surface)
        
    def update(self, ticks, nearby_tiles):
        if self._obj != None:
            self._obj.update(ticks, nearby_tiles, self)
           
    
    def __repr__(self):
        string = str(self._pos) + "is clear: " + str(self.is_clear())
        return string