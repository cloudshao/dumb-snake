from collections import deque
from instructions import Instructions, DIRECTIONS, SPEED_CHANGES, TURNS
import itertools
import logging
import operator
import time

DIRECTION_DELTAS = {
    Instructions.RIGHT: (1, 0),
    Instructions.DOWN: (0, 1),
    Instructions.LEFT: (-1, 0),
    Instructions.UP: (0, -1),
}

DIRECTION_OPPOSITES = {
    Instructions.RIGHT: Instructions.LEFT,
    Instructions.DOWN: Instructions.UP,
    Instructions.LEFT: Instructions.RIGHT,
    Instructions.UP: Instructions.DOWN,
}

# Given we're already going in a direction, what do left/right mean?
DIRECTION_TURNS = {
    None: {
        Instructions.TURN_LEFT: Instructions.LEFT,
        Instructions.TURN_RIGHT: Instructions.RIGHT,
    },
    Instructions.UP: {
        Instructions.TURN_LEFT: Instructions.LEFT,
        Instructions.TURN_RIGHT: Instructions.RIGHT,
    },
    Instructions.DOWN: {
        Instructions.TURN_LEFT: Instructions.RIGHT,
        Instructions.TURN_RIGHT: Instructions.LEFT,
    },
    Instructions.LEFT: {
        Instructions.TURN_LEFT: Instructions.DOWN,
        Instructions.TURN_RIGHT: Instructions.UP,
    },
    Instructions.RIGHT: {
        Instructions.TURN_LEFT: Instructions.UP,
        Instructions.TURN_RIGHT: Instructions.DOWN,
    },
}

class Snake():

    def __init__(self, position):
        # Right side of deque (index -1) is the head
        self.deque = deque()
        self.deque.append(position)
        self.last_update = 0.0
        self.time_between_updates = 0.1
        self.dir = None
        self.amount_to_grow = 0
        self.is_active = True

    def render(self, window):
        maxyx = window.getmaxyx()
        for x, y in self.deque:
            if 0 < y < maxyx[0] and 0 < x < maxyx[1]:
                window.addstr(y, x, "█")

    def process_instruction(self, instruction):
        if instruction in DIRECTIONS:
            self._change_dir(instruction)
        elif instruction in SPEED_CHANGES:
            if instruction == Instructions.SPEED_UP:
                self._change_speed(0.1)
            elif instruction == Instructions.SPEED_DOWN:
                self._change_speed(-0.1)
        elif instruction in TURNS:
            self._turn(instruction)

    def _turn(self, direction):
        # Compute the absolute direction
        direction = DIRECTION_TURNS[self.dir][direction]
        self.dir = direction

    def _change_dir(self, direction):
        # Don't allow going in the opposite direction
        if direction in DIRECTION_OPPOSITES and self.dir == DIRECTION_OPPOSITES[direction]:
            return

        self.dir = direction

    def _change_speed(self, delta):
        self.time_between_updates -= delta

    def grow(self):
        self.amount_to_grow +=6

    def self_intersects(self):
        head = self.deque[-1]
        all_except_head = list(itertools.islice(self.deque, 0, len(self.deque)-1))
        return head in all_except_head

    def update(self):

        if not self.is_active:
            return

        # Is it time to move yet?
        currtime = time.time()
        if currtime - self.last_update < self.time_between_updates:
            return

        # Does the snake not yet have a direction? (before game start)
        if not self.dir:
            return

        self.last_update = currtime

        # Calculate the new head
        head = self.deque[-1]
        newhead = tuple(map(operator.add, head, DIRECTION_DELTAS[self.dir]))
        self.deque.append(newhead)

        # If the snake should grow, then keep the tail
        if self.amount_to_grow:
            self.amount_to_grow -= 1
        else:
            self.deque.popleft()

        logging.debug(f"Snake: {self.deque}")

    def get_head_position(self):
        return self.deque[-1]
