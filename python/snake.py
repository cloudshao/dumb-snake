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

class Snake():

    def __init__(self, position):
        # Right side of deque (index -1) is the head
        self.deque = deque()
        self.deque.append(position)
        self.last_update = 0.0
        self.dir = None
        self.amount_to_grow = 0

    def render(self, window):
        for x, y in self.deque:
            # TODO: this should be relative to the board's coorindates
            window.addstr(y, x, "o")

    def change_dir(self, direction):
        assert(direction in Directions)
        self.dir = direction

    def grow(self):
        self.amount_to_grow +=4

    def self_intersects(self):
        head = self.deque[-1]
        # TODO: could be done without creating new list
        all_except_head = list(itertools.islice(self.deque, 0, len(self.deque)-1))
        return head in all_except_head

    def update(self):

        # Is it time to move yet?
        currtime = time.time()
        if currtime - self.last_update < 0.125:
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
