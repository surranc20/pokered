import json
from os.path import join


class ScriptingEngine():
    SCRIPTING_COMMANDS = ["MOVE", "DIALOG", "BATTLE", "TURN", "PLAY_MUSIC"
                          "FOREGROUND_CHANGE", "BACKGROUND_CHANGE", "LOCK",
                          "RELEASE"]

    def __init__(self, script, level):
        """Creates the scripting engine for a given script"""
        self._script = script
        self._level = level

    def execute_scipt_line(self):
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
                self._level.current_script = None

    def _parse_current_line(self):
        """Parses current line to determine what action needs to be taken.
        Returns the command for the line as well as the command's arguments"""
        split_line = self._script.current_line.strip().split("-")
        command, args = split_line[0], split_line[1]
        if command not in self.SCRIPTING_COMMANDS:
            raise Exception("Unknown command in script")
        return command, args

    def move(self, args):
        """Moves the trainer to a given tile. Trainers can only move
        in one direction at a time"""
        pass

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
        """Changes the foreground image to the one specefied in
        args"""
        pass

    def background_change(self, args):
        """Changes the background image to the one specified in
        args"""
        pass


class Script():
    def __init__(self, script_name):
        """Creates the script object"""
        self._script = self._load_script(script_name)
        self._current_line = 0

    def _load_script(self, script_name):
        """Loads a script."""
        if script_name not in self._scripts:
            raise Exception("Script does not exist" + script_name)

        # Generate the script path and then load the script.
        script_path = join("levels", self._level_name, script_name)
        with open(script_path, "r") as script:
            return json.load(script)

    def increment_script_line(self):
        """Adds 1 to the current script line and return True. If there
        are no more lines left in the script then return False"""
        if self._current_line >= len(self._script):
            return False
        else:
            self._current_line += 1

    @property
    def current_line(self):
        """Gets the current line of the script."""
        return self._script[self._current_line]
