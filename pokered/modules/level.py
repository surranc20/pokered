import json
from math import ceil
from os.path import join
from .trainer import Trainer
from .player import Player
from .nurse import Nurse
from .clerk import Clerk
from .pokemon import Pokemon
from .utils.scripting_engine import ScriptingEngine
from .utils.UI.drawable import Drawable
from .utils.UI.tileset_tile import TilesetTile
from .utils.UI.tileset_animated_tile import TilesetAnimatedTile
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

        # Load the data for the level.
        with open(join("levels", level_name, "meta.json"), "r") as level_json:
            self._level_meta = json.load(level_json)
            self._level_size = (self.TILE_SIZE * self._level_meta["size"][0],
                                self.TILE_SIZE * self._level_meta["size"][1])
            self._more_info = self._level_meta.get("more_info", {})
            self._doors = self._level_meta.get("doors")

        # Get all door dependent tiles
        self._door_dependents = {}
        for _, door_dependents in self._doors.items():
            status = door_dependents.get("status", "closed")
            self._door_dependents.update({tuple(door): status for door in door_dependents["dependents"]})

        # Tile the level up into 16x16 tiles.
        self.tiles = self._tile()

        # Populate the level with its trainers.
        self.populate_trainers()

        # Start the music for the level.
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)

        # Get the list of scripts for the level.
        self._scripts = self._level_meta["scripts"]
        self.current_scripting_engine = None
        self.current_script_line_debug = 0

        # If the level has an entry script that activate the script at the
        # start of the level.
        if "entry_script.json" in self._scripts:
            self.current_scripting_engine = \
                ScriptingEngine("entry_script.json", self)

    def _tile(self):
        tiles = []
        with open(join("levels", self.level_name, f"{self.level_name}_tiled.json"), "r") as tile_map_json:
            tile_map = json.load(tile_map_json)['mapArray']
            for y, map_row in enumerate(tile_map):
                row = []
                if len(map_row) < 15:
                    self.x_offset = ceil((15 - len(map_row)) / 2)
                else:
                    self.x_offset = 0
                for x, tile in enumerate(map_row):
                    if "(" + str(x) + "," + str(y) + ")" in self._doors:
                        row.append(DoorMaster((x + self.x_offset, y),
                                   tile['tileBackground'],
                                   self._doors["(" + str(x) + "," + str(y) + ")"]["dependents"],
                                   self._doors["(" + str(x) + "," + str(y) + ")"]["destination"],
                                   status=self._doors["(" + str(x) + "," + str(y) + ")"].get("status", "closed")))

                    elif (x, y) in self._door_dependents:
                        row.append(DoorDependent((x + self.x_offset, y),
                                   tile['tileBackground'], status=self._door_dependents[(x, y)]))

                    else:
                        row.append(Tile(
                            (x + self.x_offset, y),
                            tile['collidable'], None,
                            self._more_info.get("(" + str(x) + "," + str(y) + ")"),
                            tile['tileBackground']))

                for _ in range(self.x_offset):
                    row.insert(0, BlackTile((0, y)))
                    row.append(BlackTile((len(row), y)))
                tiles.append(row)

        for tile_row in tiles:
            for tile in tile_row:
                if tile.link is not False:
                    tile.link = tiles[tile.link[1]][tile.link[0]]

        return tiles

    def play_music(self):
        """Play the level's music. Can be called by the level manager."""
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)

    def reload(self):
        self.foreground.center_with_border(self.screen_size)
        self.background.center_with_border(self.screen_size)
        SoundManager.getInstance().playMusic("gym_music.mp3", -1, .5)

    def populate_trainers(self):
        """Adds the level's trainers to the level (including the player)."""
        # Add the player to the level by getting the player's start position
        # from the level's meta data.
        start_pos = self._level_meta["start_location"]
        self.player.setPosition(self.correct_border_and_heightpos(start_pos, True))
        self.tiles[self._level_meta["start_location"][1]][start_pos[0] + self.x_offset].add_obj(self.player)
        self.player.current_tile = self.tiles[start_pos[1]][start_pos[0] + self.x_offset]

        # Add the rest of the trainers to the level. Get's data from the
        # level's meta data.
        for trainer_args in self._level_meta["trainers"]:
            if trainer_args["name"] == "nurse":
                train = \
                    Nurse(self.correct_border_and_heightpos(trainer_args["pos"]),
                          trainer_args["orientation"])
            elif trainer_args["name"] == "clerk":
                train = \
                    Clerk(self.correct_border_and_heightpos(trainer_args["pos"]),
                          trainer_args["orientation"],
                          trainer_args["inventory"])
            # elif trainer_args["name"] in ["guard"]:
            #     train = \
            #         NPC(trainer_args["name"], trainer_args["pos"],
            #             trainer_args["orientation"])
            else:
                train = \
                    Trainer(self.correct_border_and_heightpos(trainer_args["pos"]),
                            trainer_args["name"],
                            trainer_args["orientation"],
                            enemy=True,
                            dialogue_id=trainer_args.get("dialogue"),
                            battle_dialogue_id=trainer_args.get("battle_dialogue"),
                            post_battle_dialogue_id=trainer_args.get("post_battle_dialogue"),
                            gender=trainer_args.get("gender", "male"),
                            train_type=trainer_args.get("trainer_type", trainer_args["name"])
                            )

                # If the trainer has an event specified in the meta data then
                # add that event.
                if len(trainer_args) > 4:
                    train.event = trainer_args["event"]

                # Calculates the stats of each of the trainer's pokemon.
                stat_calc = StatCalculator()
                if trainer_args.get("party") is not None:
                    for pokemon in trainer_args["party"]:
                        new_pokemon = Pokemon(pokemon[0],
                                              enemy=True,
                                              move_set=pokemon[1])
                        new_pokemon.stats = stat_calc.calculate_main(new_pokemon,
                                                                     pokemon[2])
                        train.pokemon_team.append(new_pokemon)

            # Add the trainer to the tile.
            self.tiles[trainer_args["pos"][1]][trainer_args["pos"][0] + self.x_offset].add_obj(train)
            train.current_tile = \
                self.tiles[trainer_args["pos"][1]][trainer_args["pos"][0] + self.x_offset]
            self.trainers[train.name] = train

    def draw(self, draw_surface):
        """Draws the level. Calls draw on each of the tiles in the level."""
        for row in self.tiles:
            for tile in row:
                tile.draw_background(draw_surface)

        for row in self.tiles:
            for tile in row:
                tile.draw_obj(draw_surface)

        for row in self.tiles:
            for tile in row:
                tile.draw_foreground(draw_surface)

    def update(self, ticks):
        """Updates the level. Updates each of the tiles in the level. If there
        is a current script active, then also update that script."""
        if self.current_scripting_engine is not None:
            print(ticks)
            if self.current_script_line_debug != self.current_scripting_engine._script._current_line:
                print("starting new task")
                self.current_script_line_debug = self.current_scripting_engine._script._current_line
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
        tile_dims = (len(self.tiles[0]),
                     len(self.tiles))
        if pos[0] < 0 or pos[1] < 0:
            return False
        elif pos[0] >= tile_dims[0] or pos[1] >= tile_dims[1]:
            return False
        else:
            return True

    def correct_border_and_heightpos(self, pos, is_player=False):
        """The player is 22 pixels high so we need to adjust his position down
        a little when first loading the level. """
        if is_player:
            return Vector2((pos[0] + self.x_offset) * self.TILE_SIZE,
                           pos[1] * self.TILE_SIZE - 6)
        else:
            return Vector2((pos[0] + self.x_offset) * self.TILE_SIZE,
                           pos[1] * self.TILE_SIZE - 8)


class Tile:
    def __init__(self, pos, collidable, obj, more_info, background_info):
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
        self.collidable = collidable
        self.link = False
        # Some tiles have extra information
        if more_info is not None:

            # Check to see if tile is a link tile (i.e a tile in front of a
            # shop seller or nurse joy). If it is a link tile then when a talk
            # is trigerred with this tile it will link to the nurse or shop
            # seller
            if "link" in more_info:
                self.link = more_info.split("-")[1].split(",")
                self.link = tuple(int(x) for x in self.link)

        # TILEMAP BELOW
        self.background_tile = TilesetTile(background_info,
                                           [pos[0] * 16, pos[1] * 16])
        self.foreground_tile = self.background_tile.create_foreground()

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

    def draw_background(self, draw_surface):
        """Draws the tile's obj if one exists. First draw background then draw obj."""
        self.background_tile.draw(draw_surface)

    def draw_foreground(self, draw_surface):
        if self.foreground_tile is not None:
            self.foreground_tile.draw(draw_surface)

    def draw_obj(self, draw_surface):
        if self._obj is not None:
            self._obj.draw(draw_surface)

    def update(self, ticks, nearby_tiles):
        """Updates the tiles obj if one exists."""
        if self._obj is not None:
            self._obj.update(ticks, nearby_tiles, self)

    def talk_event(self, player):
        """Returns tile's talk event. Will returned linked tile's talk event
        if a link exists."""
        if self.link is not False:
            return self.link.talk_event(player)
        elif self._obj is not None and self._obj is not player:
            return self._obj.talk_event(player)
        else:
            return None

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
        return str(self.pos)


class BlackTile(Tile):
    def __init__(self, pos):
        background_info = {'rowNum': 0, 'columnNum': 0,
                           'tileSetName': 'black.png'}
        super().__init__(pos, 1, None, None, background_info)


class DoorTile(Tile):

    OPENING_SOUNDS = {
        "tileset_66.png": {
            (3, 10): "firered_0012.wav"
        }
    }
    CLOSING_SOUNDS = {
        "tileset_66.png": {
            (3, 11): "firered_0026.wav",
            (1, 30): "firered_0026.wav",
            (4, 30): "firered_0026.wav",
            (7, 30): "firered_0026.wav"
        }
    }

    def __init__(self, pos, background_info, status):
        super().__init__(pos, 1, None, None, background_info)

        # Correct the door tile foreground background pixel
        self.background_tile = TilesetAnimatedTile(background_info, [pos[0] * 16, pos[1] * 16])
        self.foreground_tile = self.background_tile.create_foreground()

        # Start the door off in the right position (opened or closed)
        self.status = status
        if self.status == "open":
            self.background_tile._frame = self.background_tile._nFrames - 1
            self.background_tile.get_current_frame()
            self.foreground_tile._frame = self.foreground_tile._nFrames - 1
            self.foreground_tile.get_current_frame()
            self.collidable = False

        # Doors should not start off animated
        self.background_tile._animate = False
        self.foreground_tile._animate = False

        # Variable to keep track of if door is closing or opening
        self.opening = False
        self.closing = False

    def update(self, ticks, nearby_tiles):
        if self.background_tile._animate:
            # Door has finished opening
            if self.opening and self.background_tile._frame == self.background_tile._nFrames - 1:
                self.background_tile._animationTimer = 0
                self.background_tile._animate = False
                self.foreground_tile._animationTimer = 0
                self.foreground_tile._animate = False
                self.collidable = False
                self.opening = False

            # Door has finished closing
            elif self.closing and self.background_tile._frame == 0:
                self.background_tile._animationTimer = 0
                self.background_tile._animate = False
                self.foreground_tile._animationTimer = 0
                self.foreground_tile._animate = False
                self.collidable = True
                self.closing = False
                self.status = "closed"

            else:
                self.background_tile.update(ticks)
                self.foreground_tile.update(ticks)

        super().update(ticks, nearby_tiles)

    def open_door(self):
        self.opening = True
        self.background_tile.backwards = False
        self.foreground_tile.backwards = False
        self.background_tile.startAnimation()
        self.foreground_tile.startAnimation()

    def close_door(self):
        self.closing = True
        self.foreground_tile.backwards = True
        self.background_tile.backwards = True
        self.background_tile.startAnimation()
        self.foreground_tile.startAnimation()


class DoorMaster(DoorTile):
    def __init__(self, pos, background_info, dependents, warp_destination, status="closed"):
        super().__init__(pos, background_info, status)
        self.dependents = dependents
        if warp_destination is not None:
            self.set_warp(warp_destination)
            if status == "closed":
                self.collidable = True

        # Get opening and closing sounds
        door_key = (background_info["columnNum"], background_info["rowNum"])

        self.opening_sound = self.OPENING_SOUNDS[background_info["tileSetName"]].get(door_key)
        self.closing_sound = self.CLOSING_SOUNDS[background_info["tileSetName"]].get(door_key)

    def update(self, ticks, nearby_tiles):
        if self.closing and self.background_tile._frame == 0:
            if self.closing_sound is not None:
                SoundManager.getInstance().playSound(self.closing_sound, sound=1)

        super().update(ticks, nearby_tiles)

    def open_door(self):
        if self.opening_sound is not None:
            SoundManager.getInstance().playSound(self.opening_sound, sound=1)
        super().open_door()


class DoorDependent(DoorTile):
    def __init__(self, pos, background_info, status="closed"):
        super().__init__(pos, background_info, status)
