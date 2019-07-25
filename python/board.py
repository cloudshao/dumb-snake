import logging

GAME_OVER_TEXT = "GAME OVER"

class Board():

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.game_over = False

    def is_outside_bounds(self, pos):
        x, y = pos
        if x < 0 or x >= self.w:
            return True
        if y < 0 or y >= self.h:
            return True

        return False

    def render(self, window):
        if self.game_over:
            center_x = int(self.w/2)
            center_y = int(self.h/2)
            text_offset = int(len(GAME_OVER_TEXT)/2)
            window.addstr(center_y, center_x-text_offset, GAME_OVER_TEXT)
        # top and bottom borders
        #for i in range(self.w):
            #logging.info("addstr {0},{1}".format(0, i))
            #window.addstr(0, i, "X")
            #window.addstr(self.h-1, i, "X")
        # left and right borders
        #for j in range(self.h):
            #logging.info("addstr {0},{1}".format(j, 0))
            #window.addstr(j, 0, "X")
            #window.addstr(j, self.w-1, "X")
