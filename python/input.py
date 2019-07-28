import exceptions
import logging
import voice_input
from instructions import Instructions

INPUT_TO_DIRECTION = {
    "KEY_UP": Instructions.UP,
    "KEY_LEFT": Instructions.LEFT,
    "KEY_DOWN": Instructions.DOWN,
    "KEY_RIGHT": Instructions.RIGHT,
}

CMD_TO_DIRECTION = {
    "up": Instructions.UP,
    "left": Instructions.LEFT,
    "down": Instructions.DOWN,
    "right": Instructions.RIGHT,
}

CMD_TO_INSTRUCTION = {
    "[": Instructions.SPEED_DOWN,
    "]": Instructions.SPEED_UP,
}


def _is_prefix_of_cmd(string):
    # Could use a Trie here for slightly better performance
    for key in CMD_TO_DIRECTION:
        if key.startswith(string):
            return True
    return False


class Input:

    def __init__(self):
        self.command_line = ""
        self.voice_enabled = False

    def _get_keyboard_input(self, window):
        # Get a key from the keyboard
        user_input = None
        try:
            user_input = window.getkey()
            logging.debug(f"userinput: {user_input}")
        except Exception as e:
            pass

        # If it's v, toggle voice on/off
        if user_input == "v":
            self.voice_enabled = not self.voice_enabled

        # If it's an instruction, return it immediately
        if user_input in CMD_TO_INSTRUCTION:
            return CMD_TO_INSTRUCTION[user_input]

        # If it's a left/right/up/down direction, translate and return it
        if user_input in INPUT_TO_DIRECTION:
            direction = INPUT_TO_DIRECTION[user_input]
            return direction

        # If it's a valid letter, add it to the command_line
        if user_input and user_input.isalpha():
            new_command_line = self.command_line + user_input
            logging.debug(f"Got char: {user_input}, new command line: {new_command_line}")
            if _is_prefix_of_cmd(new_command_line):
                self.command_line = new_command_line

        # If it's the enter key, process what's on the command_line
        if user_input == "\n":
            command = self.command_line
            self.command_line = ""
            if command in CMD_TO_DIRECTION:
                return CMD_TO_DIRECTION[command]

        return None

    def get_instruction(self, window):
        # Try getting voice input
        if self.voice_enabled:
            try:
                instruction = voice_input.get_instruction()
                return instruction
            except exceptions.NoInputException:
                pass

        # Try getting keyboard input
        key_input = self._get_keyboard_input(window)
        if key_input:
            return key_input

        raise exceptions.NoInputException

    def render(self, window):
        size = window.getmaxyx()
        window.addstr(size[0]-1, 0, self.command_line)
        if self.voice_enabled:
            window.addstr(size[0]-1, 10, "voice")
