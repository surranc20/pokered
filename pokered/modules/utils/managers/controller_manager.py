class ControllerManager():
    def __init__(self, controller, threshold):
        """Creates a controller manager which can map controller inputs to
        keyboard inputs."""
        self.threshold = threshold
        self.controller = controller
        self._previous_input = None
        self.previous_input = None
        self.input_valid = True

    def parse_input(self, controller):
        """Takes a given input from a contoller, normalizes, and returns the
        parsed data"""
        self.previous_input = self._previous_input
        joycon_input = self.normalize_joystick(controller)
        parsed_input = []
        if 0 not in joycon_input:
            if self._previous_input is None:
                parsed_input = [joycon_input[0], 0]
            else:
                # One of the previous inputs will match
                parsed_input = self._get_match(joycon_input)
        else:
            parsed_input = joycon_input

        self._previous_input = parsed_input

        if self.previous_input != parsed_input:
            self.input_valid = True
        else:
            self.input_valid = False

        return parsed_input

    def normalize_joystick(self, controller):
        """Normalizes joystick inputs to -1, 0, or 1"""
        joycon_input = [controller.get_axis(0), controller.get_axis(1)]
        normalized_input = []
        prev = float('-inf')
        for value in joycon_input:

            if abs(value) < self.threshold:
                value = 0
            else:
                # If values are +- > threshold then we want the larger value.
                # If they are both 1/-1 then we will handle this case later.
                if abs(value) >= prev:
                    prev = abs(value)
                else:
                    value = 0

                if value < 0:
                    value = -1
                elif value > 0:
                    value = 1

            normalized_input.append(value)
        return normalized_input

    def get_joystick_data(self):
        """Parses data from controller and returns the corresponding pygame
        keydown event."""
        parsed_joystick_values = self.parse_input(self.controller)

        if parsed_joystick_values[0] == 1 or \
                (parsed_joystick_values == [0, 0] and
                    self.previous_input == [1, 0]):
            event_dict = {'unicode': 'd', 'key': 100, 'mod': 0, 'scancode': 2}
        elif parsed_joystick_values[0] == -1 or \
                (parsed_joystick_values == [0, 0] and
                    self.previous_input == [-1, 0]):
            event_dict = {'unicode': 'a', 'key': 97, 'mod': 0, 'scancode': 0}
        elif parsed_joystick_values[1] == 1 or \
                (parsed_joystick_values == [0, 0] and
                    self.previous_input == [0, 1]):
            event_dict = {'unicode': 's', 'key': 115, 'mod': 0, 'scancode': 1}
        elif parsed_joystick_values[1] == -1 or \
                (parsed_joystick_values == [0, 0] and
                    self.previous_input == [0, -1]):
            event_dict = {'unicode': 'w', 'key': 119, 'mod': 0, 'scancode': 13}
        elif parsed_joystick_values == [0, 0] and \
                (self.previous_input == [0, 0] or self.previous_input is None):
            self.input_valid = False
            event_dict = {}

        else:
            print(f"{parsed_joystick_values} {self.previous_input}")
            raise Exception

        # Is the axis "on" or "off" based on the threshold
        biggest_move = max([abs(value) for value in parsed_joystick_values])
        if biggest_move > self.threshold:
            event_data = (2, event_dict)
        else:
            event_data = (3, event_dict)

        return event_data

    def _get_match(self, current_input):
        """Looking back at this I don't understand why this doesn't always
        return something and I do not have access to a controller at the
        moment to test. Appears to see if any of the inputs directions match
        the controllers prevoius input."""
        prev_set = None
        for index, value in enumerate(self._previous_input):
            if value != 0:
                prev_set = index
        if prev_set is None:
            return [0, 0]

        matched_input = current_input
        for index in range(len(current_input)):
            if index == prev_set:
                matched_input[index] = current_input[index]
            else:
                matched_input[index] = 0

        return matched_input

    def get_button_data(self, event):
        """Returns pygame event info for button presses."""
        self.input_valid = True
        button_map = {
            2: {'unicode': '\\r',  'key': 13, 'mod': 0, 'scancode': 36},
            1: {'unicode': 'b',  'key': 98, 'mod': 0, 'scancode': 11},
            9: {'unicode': '',  'key': 303, 'mod': 0, 'scancode': 0}
        }
        response = button_map.get(event.button)
        if response is None:
            self.input_valid = False
        return response
