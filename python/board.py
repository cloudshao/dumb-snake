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
