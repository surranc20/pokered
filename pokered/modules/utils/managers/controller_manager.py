class ControllerManager():
    def __init__(self, controller, threshold):
        self.threshold = threshold
        self.controller = controller
        self._previous_input = None
        self.previous_input = None
        self.input_valid = True



    def parse_input(self, controller):
        self.previous_input = self._previous_input
        print(f"previous before: {self.previous_input}")
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
        print(f"previous after: {self.previous_input}")

        if self.previous_input != parsed_input:
            self.input_valid = True
        else:
            self.input_valid = False

        return parsed_input

    def normalize_joystick(self, controller):
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

    def _get_match(self, current_input):
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


