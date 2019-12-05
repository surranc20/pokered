import json
import pygame
from os.path import join
from .trainer import Trainer
from .player import Player
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
        self._level_name = level_name
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
        self._scripts = self._level_meta[4]
        self._current_script = None
        if "entry_script.json" in self._scripts:
            self.load_script("entry_script.json")

    
    def _tile(self):
        
        tile_dims = (self._level_size[0] // self.TILE_SIZE, self._level_size[1] // self.TILE_SIZE)
        
        tiles = []
        
        for y in range(tile_dims[1]):
            row = []
            for x in range(tile_dims[0]):
                row.append(Tile((x,y), self._colide_list[y][x], None))
            tiles.append(row)
        
        return tiles
    
    def play_music(self):
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)


    def populate_trainers(self):
        self._player.setPosition(self.correct_border_and_height_pos(self._level_meta[1]))
        self._tiles[self._level_meta[1][1]][self._level_meta[1][0]].add_obj(self._player)
        self._player._current_tile = self._tiles[self._level_meta[1][1]][self._level_meta[1][0]]
        for trainer_args in self._level_meta[2]:
            train = Trainer(self.correct_border_and_height_pos(trainer_args[0]), trainer_args[1], trainer_args[2], enemy=True, dialogue_id=trainer_args[2], gender=trainer_args[5])
            if len(trainer_args) > 4:
                train._event = trainer_args[4]
            for pokemon in trainer_args[3]:
                train._pokemon_team.append(Pokemon(pokemon[0], enemy=True, move_set=pokemon[1]))
            self._tiles[trainer_args[0][1]][trainer_args[0][0]].add_obj(train)


    def draw(self, draw_surface):
        self._background.draw(draw_surface)
        for row in self._tiles:
            for tile in row:
                tile.draw(draw_surface)
        self._foreground.draw(draw_surface)
    
    def update(self, ticks):
        if self._current_script != None:
            self.execute_script_line()
        for y, row in enumerate(self._tiles):
            for x, tile in enumerate(row):
                tile.update(ticks, self.get_nearby_tiles((x,y)))
                if tile.warp_triggered():
                    return tile.get_warp_level()
        
        Drawable.updateWindowOffset(self._player, self._screen_size, self._level_size)
    
    def execute_script_line(self):
        try:
            if eval(str(self._current_script[0][self._current_script[1]])) != False:
                self._current_script[1] +=1
                if self._current_script[1] + 1 > len(self._current_script[0]):
                    self._current_script = None
        except Exception as e:
            print(e)
            exec(str(self._current_script[0][self._current_script[1]]))
            self._current_script[1] +=1
            if self._current_script[1] + 1 > len(self._current_script[0]):
                self._current_script = None


    
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
    
    def load_script(self, script_name):
        if script_name != "None" and script_name not in self._scripts:
            print(script_name)
            raise Exception
        
        elif script_name != "None":
            with open(join("levels", self._level_name, script_name), "r") as script:
                self._current_script = [json.load(script), 0]


class Tile:
    def __init__(self, pos, colidable, obj):
        self._pos = pos
        self._obj = obj
        self._base_colidable = colidable
        self._is_warp = False
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

    def set_warp(self, level_name):
        self._colidable = False
        self._is_warp = True
        self._warp_level = level_name
    
    def warp_triggered(self):
        return self._is_warp and type(self._obj) == Player
    
    def get_warp_level(self):
        return self._warp_level
            
    
    
           
    
    def __repr__(self):
        string = str(self._pos) + "is clear: " + str(self.is_clear())
        return string