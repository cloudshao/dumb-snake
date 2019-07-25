from enum import Enum

class Directions(Enum):
    # TODO rename, these are more generalized inputs and not just directions
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4

class Instructions(Enum):
    SPEED_UP = 1
    SPEED_DOWN = 2
