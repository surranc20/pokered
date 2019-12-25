import json
import pygame
import logging
from ast import literal_eval as make_tuple
from os.path import join
from .managers.soundManager import SoundManager
from .UI.drawable import Drawable
from ..events.dialogue import Dialogue

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ScriptingEngine():
    SCRIPTING_COMMANDS = ["MOVE", "DIALOGUE", "BATTLE", "TURN", "PLAY_MUSIC",
                          "FOREGROUND_CHANGE", "BACKGROUND_CHANGE", "LOCK",
                          "RELEASE", "PLAY_SOUND", "SET_WARP"]

    def __init__(self, script_name, level):
        """Creates the scripting engine for a given script"""
        self._script = Script(script_name, level)
        self._level = level

    def execute_script_line(self):
        """Executes a given script line. If the line is not done
        executing then the engine will wait (i.e. player walking to
        a specific tile.)"""
        command, args = self._parse_current_line()

        # Execute the method associated with the given command.
        # If the method does not return False (i.e. is done executing)
        # then increment the scripts line.
        response = getattr(self, command.lower())(args)
        if response is not False:
            # Increment the script line. If all lines have been executed
            # then set the level's current script to None.
            # The current script is now over.
            if not self._script.increment_script_line():
                self._level.current_scripting_engine = None
            return response

    def _parse_current_line(self):
        """Parses current line to determine what action needs to be taken.
        Returns the command for the line as well as the command's arguments"""
        split_line = self._script.current_line.strip().split(" ")
        # Get the command from the script. This will always be the
        # first word.
        command = split_line[0]
        # Get the arguments from the script. These are seperated by a comma.
        args = split_line[1:]

        if command not in self.SCRIPTING_COMMANDS:
            raise Exception("Unknown command in script", command)
        return command, args

    def move(self, args):
        """Moves the trainer to a given tile. Trainers can only move
        in one direction at a time"""
        if len(args) != 2:
            raise Exception("Expected args of len 2:", args)

        target_pos = make_tuple(args[1])

        if args[0] == "PLAYER":
            response = self._level.player.move_to_tile(target_pos)
        else:
            response = \
                self._level.trainers[args[0]].move_to_tile(target_pos)

        return response is True

    def dialogue(self, args):
        """Creates a dialogue event between the player and the trainer."""
        print(args)
        npc = self._level.trainers[args[0]]
        return Dialogue(args[1], self._level.player, npc)

    def battle(self, args):
        """Creates a battle event between the player and the trainer."""
        pass

    def turn(self, args):
        """Turns a trainer to the given direction."""
        pass

    def lock(self, args):
        """Locks in the player so that they can not move."""
        pass

    def release(self, args):
        """Releases the player so that they can move again"""
        pass

    def play_music(self, args):
        """Plays the level's music"""
        pass

    def play_sound(self, args):
        """Plays a sound effect"""
        if len(args) != 1:
            raise Exception("Expected args of len 1:", args)

        SoundManager.getInstance().playSound(args[0], sound=1)
        return True

    def foreground_change(self, args):
        """Changes the foreground image to the one specefied in args"""
        try:
            self._level.foreground = \
                Drawable(join(self._level.level_name, args[0]), (0, 0))
            self._level.foreground.center_with_border(self._level.screen_size)
        except pygame.error as e:
            print(e)
        return True

    def background_change(self, args):
        """Changes the background image to the one specified in
        args"""
        try:
            self._level.background = \
                Drawable(join(self._level.level_name, args[0]), (0, 0))
            self._level.background.center_with_border(self._level.screen_size)
        except pygame.error as e:
            print(e)
        return True

    def set_warp(self, args):
        """Sets a tile position to warp to a given location."""
        self._level.tiles[int(args[1])][int(args[0])].set_warp(args[2])


class Script():
    def __init__(self, script_name, level):
        """Creates the script object"""
        self._current_line = 0
        self._level = level
        self._script = self._load_script(script_name, level.level_name)

    def _load_script(self, script_name, level_name):
        """Loads a script."""
        if script_name.split()[0] == "after_battle_dialog":
            return self._after_battle_dialog(script_name)
        else:
            try:
                # Generate the script path and then load the script.
                script_path = join("levels", level_name, script_name)
                with open(script_path, "r") as script:
                    return json.load(script)
            except Exception as e:
                print("Error loading script")
                print(e)

    def increment_script_line(self):
        """Adds 1 to the current script line and return True. If there
        are no more lines left in the script then return False"""
        if self._current_line >= len(self._script) - 1:
            return False
        else:
            self._current_line += 1
            return True

    @property
    def current_line(self):
        """Gets the current line of the script."""
        return self._script[self._current_line]

    def _after_battle_dialog(self, script_name):
        script = script_name.split(" ")
        return [
            "DIALOGUE " + script[1] + " " + script[2]
        ]
