from collections import deque
from directions import Directions
import itertools
import logging
import operator
import time

DIRECTION_DELTAS = {
    Directions.RIGHT: (1, 0),
    Directions.DOWN: (0, 1),
    Directions.LEFT: (-1, 0),
    Directions.UP: (0, -1),
}

DIRECTION_OPPOSITES = {
    Directions.RIGHT: Directions.LEFT,
    Directions.DOWN: Directions.UP,
    Directions.LEFT: Directions.RIGHT,
    Directions.UP: Directions.DOWN,
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
            # TODO: this should be relative to the board's coorindates
            if 0 < y < maxyx[0] and 0 < x < maxyx[1]:
                window.addstr(y, x, "█")

    def change_dir(self, direction):
        assert(direction in Directions)

        # Don't allow a turn in the opposite direction
        if direction in DIRECTION_OPPOSITES and self.dir == DIRECTION_OPPOSITES[direction]:
            return

        self.dir = direction

    def change_speed(self, delta):
        self.time_between_updates -= delta

    def grow(self):
        self.amount_to_grow +=6

    def self_intersects(self):
        head = self.deque[-1]
        # TODO: could be done without creating new list
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

        #logging.info(f"Snake: {self.deque}")

    def get_head_position(self):
        return self.deque[-1]
