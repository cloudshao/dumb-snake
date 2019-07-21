import exceptions
import logging
from directions import Directions

INPUT_TO_DIRECTION = {
    "KEY_UP": Directions.UP,
    "KEY_LEFT": Directions.LEFT,
    "KEY_DOWN": Directions.DOWN,
    "KEY_RIGHT": Directions.RIGHT,
}

CMD_TO_DIRECTION = {
    "up": Directions.UP,
    "left": Directions.LEFT,
    "down": Directions.DOWN,
    "right": Directions.RIGHT,
}

def _is_prefix_of_cmd(string):
    # TODO can use a trie
    for key in CMD_TO_DIRECTION:
        if key.startswith(string):
            return True
    return False

class Input:

    def __init__(self):
        self.command_line = ""

    def _get_keyboard_direction(self, window):
        # Get a key from the keyboard
        userinput = None
        try:
            userinput = window.getkey()
            logging.info(f"userinput: {userinput}")
        except Exception as e:
            pass

        # If it's a left/right/up/down direction, translate and return it
        if userinput in INPUT_TO_DIRECTION:
            direction = INPUT_TO_DIRECTION[userinput]
            return direction

        # If it's a valid letter, add it to the command_line
        if userinput and userinput.isalpha():
            new_command_line = self.command_line + userinput
            logging.info(f"Got char: {userinput}, new command line: {new_command_line}")
            if _is_prefix_of_cmd(new_command_line):
                self.command_line = new_command_line

        # If it's the enter key, process what's on the command_line
        if userinput == "\n":
            command = self.command_line
            self.command_line = ""
            if command in CMD_TO_DIRECTION:
                return CMD_TO_DIRECTION[command]

        return None

    def get_input(self, window):
        key_input = self._get_keyboard_direction(window)
        if key_input:
            return key_input

        raise exceptions.NoInputException

    def render(self, window):
        size = window.getmaxyx()
        window.addstr(size[0]-1, 0, self.command_line)
