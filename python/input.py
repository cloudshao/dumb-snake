import exceptions
import logging
import voice_input
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
        self.voice_enabled = False

    def _get_direction(self, window):
        # Get a key from the keyboard
        userinput = None
        try:
            userinput = window.getkey()
            logging.info(f"userinput: {userinput}")
        except Exception as e:
            pass

        # If it's v, toggle voice on/off
        if userinput == "v":
            self.voice_enabled = not self.voice_enabled

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
        if userinput == " ":
            command = self.command_line
            self.command_line = ""
            if command in CMD_TO_DIRECTION:
                return CMD_TO_DIRECTION[command]

        return None

    def get_input(self, window):
        if self.voice_enabled:
            voice_command = voice_input.get_direction()
            if voice_command in CMD_TO_DIRECTION:
                return CMD_TO_DIRECTION[voice_command]

        key_input = self._get_direction(window)
        if key_input:
            return key_input

        raise exceptions.NoInputException

    def render(self, window):
        size = window.getmaxyx()
        window.addstr(size[0]-1, 0, self.command_line)
        if self.voice_enabled:
            window.addstr(size[0]-1, 10, "voice")
