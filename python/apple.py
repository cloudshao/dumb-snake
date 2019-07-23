import random

class Apple:

    def __init__(self, boardwidth, boardheight):
        self.w = boardwidth
        self.h = boardheight
        self.pos = (0,0)
        self.move()

    def move(self):
        self.pos = (random.randrange(1, self.w-2), random.randrange(1, self.h-2))

    def overlaps(self, pos):
        return self.pos == pos

    def render(self, window):
        window.addstr(self.pos[1], self.pos[0], "")
