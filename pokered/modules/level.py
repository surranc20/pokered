import json
import pygame
from os.path import join
from .trainer import Trainer
from .player import Player
from .pokemon import Pokemon
from .utils.UI.drawable import Drawable
from .utils.vector2D import Vector2
from .utils.stat_calc import StatCalculator
from .utils.soundManager import SoundManager
from .enumerated.cardinality import Cardinality

class Level():
    TILE_SIZE = 16
    def __init__(self, level_name, player, screen_size):
        """Creates a level instance. Expects the level's name, the player, and the screen size"""
        self._player = player
        self._screen_size = screen_size
        self._level_name = level_name

        # We need a foreground and background to add a 3d effect to the game.
        self._foreground = Drawable(join(level_name, "level_foreground.png"),(0,0))
        self._background = Drawable(join(level_name, "level_background.png"), (0,0))

        # Load the data for the level.
        with open(join("levels", level_name,"meta.json"), "r") as level_json:
            self._level_meta = json.load(level_json)
            self._level_size = (self.TILE_SIZE * self._level_meta[0][0], self.TILE_SIZE * self._level_meta[0][1])
            self._colide_list = self._level_meta[3]

        # Tile the level up into 16x16 tiles.
        self._tiles = self._tile()

        # Add borders to the foreground and background if the level is smaller than the screen size.
        self._foreground.center_with_border(screen_size)
        self._background.center_with_border(screen_size)

        # Populate the level with its trainers.
        self.populate_trainers()

        # Start the music for the level.
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)

        # Get the list of scripts for the level.
        self._scripts = self._level_meta[4]
        self._current_script = None

        # If the level has an entry script that activate the script at the start of the level.
        if "entry_script.json" in self._scripts:
            self.load_script("entry_script.json")


    def _tile(self):
        """Returns the level's 2d array of tiles."""
        tile_dims = (self._level_size[0] // self.TILE_SIZE, self._level_size[1] // self.TILE_SIZE)
        tiles = []
        for y in range(tile_dims[1]):
            row = []
            for x in range(tile_dims[0]):
                row.append(Tile((x,y), self._colide_list[y][x], None))
            tiles.append(row)
        return tiles

    def play_music(self):
        """Play the level's music. Can be called by the level manager."""
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)


    def populate_trainers(self):
        """Adds the level's trainers to the level (including the player)."""
        # Add the player to the level by getting the player's start position from the level's meta data.
        self._player.setPosition(self.correct_border_and_height_pos(self._level_meta[1]))
        self._tiles[self._level_meta[1][1]][self._level_meta[1][0]].add_obj(self._player)
        self._player._current_tile = self._tiles[self._level_meta[1][1]][self._level_meta[1][0]]

        # Add the rest of the trainers to the level. Get's data from the level's meta data.
        for trainer_args in self._level_meta[2]:
            train = Trainer(self.correct_border_and_height_pos(trainer_args[0]), trainer_args[1], trainer_args[2], enemy=True, dialogue_id=trainer_args[2], battle_dialogue_id= trainer_args[3], post_battle_dialogue_id=trainer_args[4], gender=trainer_args[7])
            # If the trainer has an event specified in the meta data then add that event.
            if len(trainer_args) > 4:
                train.event = trainer_args[6]
            # Calculates the stats of each of the trainer's pokemon.
            stat_calc = StatCalculator()
            for pokemon in trainer_args[5]:
                new_pokemon = Pokemon(pokemon[0], enemy=True, move_set=pokemon[1])
                new_pokemon.stats = stat_calc.calculate_main(new_pokemon, pokemon[2])
                train.pokemon_team.append(new_pokemon)
            # Add the trainer to the tile.
            self._tiles[trainer_args[0][1]][trainer_args[0][0]].add_obj(train)
            #TODO: Will also need to set the trainers active tile


    def draw(self, draw_surface):
        """Draws the level. Calls draw on each of the tiles in the level."""
        self._background.draw(draw_surface)
        for row in self._tiles:
            for tile in row:
                tile.draw(draw_surface)
        self._foreground.draw(draw_surface)

    def update(self, ticks):
        """Updates the level. Updates each of the tiles in the level. If there is a current script active, then also update that script."""
        if self._current_script != None:
            self.execute_script_line()
        for y, row in enumerate(self._tiles):
            for x, tile in enumerate(row):
                tile.update(ticks, self.get_nearby_tiles((x,y)))
                if tile.warp_triggered():
                    return tile.get_warp_level()

        Drawable.updateWindowOffset(self._player, self._screen_size, self._level_size)

    def execute_script_line(self):
        """This is a super temporary and simple scripting engine. If I decide to develop the game further this will have to be changed.
        I am well aware of the risks of usign eval and exec."""
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
        """Returns a dictionary of tiles adjacent to a tile."""
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
        """Returns whether or not a tile is within the size of the map."""
        tile_dims = (self._level_size[0] // self.TILE_SIZE, self._level_size[1] // self.TILE_SIZE)
        if pos[0] < 0 or pos[1] < 0: return False
        elif pos[0] >= tile_dims[0] or pos[1] >= tile_dims[1]: return False
        else: return True

    def correct_border_and_height_pos(self, pos):
        """The player is 22 pixels high so we need to adjust his position down a little when first loading the level. """
        return Vector2(pos[0] * self.TILE_SIZE + self._foreground._x_off, pos[1] * self.TILE_SIZE - 6)

    def load_script(self, script_name):
        """Loads a script."""
        if script_name != "None" and script_name not in self._scripts:
            print(script_name)
            raise Exception

        elif script_name != "None":
            with open(join("levels", self._level_name, script_name), "r") as script:
                self._current_script = [json.load(script), 0]


class Tile:
    def __init__(self, pos, colidable, obj):
        """Simple class representing a tile on the map. While commenting this I realized that I spelt collidable wrong. I will
        fix this later."""
        self._pos = pos
        self._obj = obj
        # We need to keep track of what the tiles colidability was at the start of the level so that we can set it back
        # to the correct state once an object leaves the tile. Also the player can sometimes begin a level in a colidable tile
        # and the tile will resume normal functionallity after the player has left said tile.
        self._base_colidable = colidable
        # A tile is a warp if occupying it sends the player to another level.
        self._is_warp = False
        self._colidable = True if colidable == 1 else False

    def add_obj(self, obj):
        """Adds an object to a tile. Usually a player or a trainer. If a tile has an object than it becomes colidable."""
        if self._obj == None:
            self._obj = obj
            self._colidable = True
        else:
            raise Exception

    def remove_obj(self):
        """Removes a tiles object and sets its colidability back to what it was at the start of the level."""
        self._obj = None
        self._colidable = self._base_colidable

    def is_clear(self):
        """Returns whether or not a tile has nothing on it and is not collidable."""
        return not self._colidable

    def draw(self, draw_surface):
        """Draws the tile's obj if one exists."""
        if self._obj != None:
            self._obj.draw(draw_surface)

    def update(self, ticks, nearby_tiles):
        """Updates the tiles obj if one exists."""
        if self._obj != None:
            self._obj.update(ticks, nearby_tiles, self)

    def set_warp(self, level_name):
        """Sets a tile as a warp tile, requires being passed in a level name that the player will warp into."""
        self._colidable = False
        self._is_warp = True
        self._warp_level = level_name

    def warp_triggered(self):
        """Determines if a warp has been triggered."""
        return self._is_warp and type(self._obj) == Player

    def get_warp_level(self):
        """Return the warp tiles warp level."""
        return self._warp_level

    def __repr__(self):
        """Allows the tile to be printed in a nice format."""
        string = str(self._pos) + "is clear: " + str(self.is_clear())
        return string