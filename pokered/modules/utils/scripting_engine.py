import json
import pygame
from ast import literal_eval as make_tuple
from os.path import join
from .UI.drawable import Drawable


class ScriptingEngine():
    SCRIPTING_COMMANDS = ["MOVE", "DIALOG", "BATTLE", "TURN", "PLAY_MUSIC",
                          "FOREGROUND_CHANGE", "BACKGROUND_CHANGE", "LOCK",
                          "RELEASE"]

    def __init__(self, script_name, level):
        """Creates the scripting engine for a given script"""
        self._script = Script(script_name, level.level_name)
        self._level = level

    def execute_script_line(self):
        """Executes a given script line. If the line is not done
        executing then the engine will wait (i.e. player walking to
        a specific tile.)"""
        command, args = self._parse_current_line()

        # Execute the method associated with the given command.
        # If the method does not return False (i.e. is done executing)
        # then increment the scripts line.
        if (getattr(self, command.lower())(args)):
            # Increment the script line. If all lines have been executed
            # then set the level's current script to None.
            # The current script is now over.
            if not self._script.increment_script_line():
                self._level.current_scripting_engine = None

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
            raise Exception("Unexpected args length: ", args)

        target_pos = make_tuple(args[1])

        if args[0] == "PLAYER":
            print(args[1])
            response = self._level.player.move_forward_to_tile(target_pos)
        return response is True

    def dialogue(self, args):
        """Creates a dialogue event between the player and the trainer."""
        pass

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
        pass


class Script():
    def __init__(self, script_name, level_name):
        """Creates the script object"""
        self._current_line = 0
        self._script = self._load_script(script_name, level_name)

    def _load_script(self, script_name, level_name):
        """Loads a script."""
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
