from enum import Enum

class Instructions(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4
    SPEED_UP = 5
    SPEED_DOWN = 6
    TURN_LEFT = 7
    TURN_RIGHT = 8


DIRECTIONS = [
    Instructions.RIGHT,
    Instructions.DOWN,
    Instructions.LEFT,
    Instructions.UP,
]

SPEED_CHANGES = [
    Instructions.SPEED_UP,
    Instructions.SPEED_DOWN,
]

TURNS = [
    Instructions.TURN_LEFT,
    Instructions.TURN_RIGHT,
]
