import json
from os.path import join
from .trainer import Trainer
from .player import Player
from .pokemon import Pokemon
from .utils.scripting_engine import ScriptingEngine
from .utils.UI.drawable import Drawable
from .utils.vector2D import Vector2
from .utils.stat_calc import StatCalculator
from .utils.managers.soundManager import SoundManager
from .enumerated.cardinality import Cardinality


class Level():
    TILE_SIZE = 16

    def __init__(self, level_name, player, screen_size):
        """Creates a level instance. Expects the level's name, the player, and
        the screen size"""
        self.player = player
        self.screen_size = screen_size
        self.level_name = level_name

        # Dictionary to track all trainers on the map
        self.trainers = {}

        # We need a foreground and background to add a 3d effect to the game.
        self.foreground = Drawable(join(level_name, "level_foreground.png"),
                                   (0, 0))
        self.background = Drawable(join(level_name, "level_background.png"),
                                   (0, 0))

        # Load the data for the level.
        with open(join("levels", level_name, "meta.json"), "r") as level_json:
            self._level_meta = json.load(level_json)
            self._level_size = (self.TILE_SIZE * self._level_meta[0][0],
                                self.TILE_SIZE * self._level_meta[0][1])
            self._colide_list = self._level_meta[3]

        # Tile the level up into 16x16 tiles.
        self.tiles = self._tile()

        # Add borders to the foreground and background if the level is smaller
        # than the screen size.
        self.foreground.center_with_border(screen_size)
        self.background.center_with_border(screen_size)

        # Populate the level with its trainers.
        self.populate_trainers()

        # Start the music for the level.
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)

        # Get the list of scripts for the level.
        self._scripts = self._level_meta[4]
        self.current_scripting_engine = None

        # If the level has an entry script that activate the script at the
        # start of the level.
        if "entry_script.json" in self._scripts:
            self.current_scripting_engine = \
                ScriptingEngine("entry_script.json", self)

    def _tile(self):
        """Returns the level's 2d array of tiles."""
        tile_dims = (self._level_size[0] // self.TILE_SIZE,
                     self._level_size[1] // self.TILE_SIZE)
        tiles = []
        for y in range(tile_dims[1]):
            row = []
            for x in range(tile_dims[0]):
                row.append(Tile((x, y), self._colide_list[y][x], None))
            tiles.append(row)
        return tiles

    def play_music(self):
        """Play the level's music. Can be called by the level manager."""
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)

    def populate_trainers(self):
        """Adds the level's trainers to the level (including the player)."""
        # Add the player to the level by getting the player's start position
        # from the level's meta data.
        self.player.setPosition(self.correct_border_and_heightpos(self._level_meta[1]))
        self.tiles[self._level_meta[1][1]][self._level_meta[1][0]].add_obj(self.player)
        self.player.current_tile = self.tiles[self._level_meta[1][1]][self._level_meta[1][0]]

        # Add the rest of the trainers to the level. Get's data from the
        # level's meta data.
        for trainer_args in self._level_meta[2]:
            train = \
                Trainer(self.correct_border_and_heightpos(trainer_args[0]),
                        trainer_args[1],
                        trainer_args[2],
                        enemy=True,
                        dialogue_id=trainer_args[3],
                        battle_dialogue_id=trainer_args[4],
                        post_battle_dialogue_id=trainer_args[5],
                        gender=trainer_args[8])

            # If the trainer has an event specified in the meta data then add
            # that event.
            if len(trainer_args) > 4:
                train.event = trainer_args[7]

            # Calculates the stats of each of the trainer's pokemon.
            stat_calc = StatCalculator()
            for pokemon in trainer_args[6]:
                new_pokemon = Pokemon(pokemon[0],
                                      enemy=True,
                                      move_set=pokemon[1])
                new_pokemon.stats = stat_calc.calculate_main(new_pokemon,
                                                             pokemon[2])
                train.pokemon_team.append(new_pokemon)

            # Add the trainer to the tile.
            self.tiles[trainer_args[0][1]][trainer_args[0][0]].add_obj(train)
            train.current_tile = \
                self.tiles[trainer_args[0][1]][trainer_args[0][0]]
            self.trainers[train.name] = train

    def draw(self, draw_surface):
        """Draws the level. Calls draw on each of the tiles in the level."""
        self.background.draw(draw_surface)
        for row in self.tiles:
            for tile in row:
                tile.draw(draw_surface)
        self.foreground.draw(draw_surface)

    def update(self, ticks):
        """Updates the level. Updates each of the tiles in the level. If there
        is a current script active, then also update that script."""
        if self.current_scripting_engine is not None:
            response = self.current_scripting_engine.execute_script_line()
            if hasattr(response, "handle_event"):
                return response
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tile.update(ticks, self.get_nearby_tiles((x, y)))
                if tile.warp_triggered():
                    return tile.get_warp_level()

        Drawable.updateWindowOffset(self.player, self.screen_size,
                                    self._level_size)

    def get_nearby_tiles(self, pos):
        """Returns a dictionary of tiles adjacent to a tile."""
        nearby_tiles = {}

        if self.tile_within_map((pos[0], pos[1] - 1)):
            nearby_tiles[Cardinality.NORTH] = self.tiles[pos[1] - 1][pos[0]]
        if self.tile_within_map((pos[0], pos[1] + 1)):
            nearby_tiles[Cardinality.SOUTH] = self.tiles[pos[1] + 1][pos[0]]
        if self.tile_within_map((pos[0] - 1, pos[1])):
            nearby_tiles[Cardinality.WEST] = self.tiles[pos[1]][pos[0] - 1]
        if self.tile_within_map((pos[0] + 1, pos[1])):
            nearby_tiles[Cardinality.EAST] = self.tiles[pos[1]][pos[0] + 1]

        return nearby_tiles

    def tile_within_map(self, pos):
        """Returns whether or not a tile is within the size of the map."""
        tile_dims = (self._level_size[0] // self.TILE_SIZE,
                     self._level_size[1] // self.TILE_SIZE)
        if pos[0] < 0 or pos[1] < 0:
            return False
        elif pos[0] >= tile_dims[0] or pos[1] >= tile_dims[1]:
            return False
        else:
            return True

    def correct_border_and_heightpos(self, pos):
        """The player is 22 pixels high so we need to adjust his position down
        a little when first loading the level. """
        return Vector2(pos[0] * self.TILE_SIZE + self.foreground._x_off,
                       pos[1] * self.TILE_SIZE - 6)


class Tile:
    def __init__(self, pos, collidable, obj):
        """Simple class representing a tile on the map. While commenting this
        I realized that I spelt collidable wrong. I will fix this later."""
        self.pos = pos
        self._obj = obj
        # We need to keep track of what the tiles colidability was at the
        # start of the level so that we can set it back to the correct state
        # once an object leaves the tile. Also the player can sometimes begin
        # a level in a colidable tile and the tile will resume normal
        # functionallity after the player has left said tile.
        self._base_colidable = collidable
        # A tile is a warp if occupying it sends the player to another level.
        self._is_warp = False
        self.collidable = True if collidable == 1 else False

    def add_obj(self, obj):
        """Adds an object to a tile. Usually a player or a trainer. If a tile
        has an object than it becomes colidable."""
        if self._obj is None:
            self._obj = obj
            self.collidable = True
        else:
            raise Exception

    def remove_obj(self):
        """Removes a tiles object and sets its colidability back to what it
        was at the start of the level."""
        self._obj = None
        self.collidable = self._base_colidable

    def is_clear(self):
        """Returns whether or not a tile has nothing on it and is not
        collidable."""
        return not self.collidable

    def draw(self, draw_surface):
        """Draws the tile's obj if one exists."""
        if self._obj is not None:
            self._obj.draw(draw_surface)

    def update(self, ticks, nearby_tiles):
        """Updates the tiles obj if one exists."""
        if self._obj is not None:
            self._obj.update(ticks, nearby_tiles, self)

    def set_warp(self, level_name):
        """Sets a tile as a warp tile, requires being passed in a level name
        that the player will warp into."""
        self.collidable = False
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
        string = str(self.pos) + "is clear: " + str(self.is_clear())
        return string
