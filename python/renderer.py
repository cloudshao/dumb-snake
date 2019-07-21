import curses
import logging
from board import Board
from snake import Snake, Directions
from apple import Apple

INPUT_TO_DIRECTION = {
    "KEY_UP": Directions.UP,
    "KEY_LEFT": Directions.LEFT,
    "KEY_DOWN": Directions.DOWN,
    "KEY_RIGHT": Directions.RIGHT,
}

class Renderer():

    def __init__(self):
        # TODO snake and board should probably be owned by a level or something
        self.window = curses.initscr()
        size = self.window.getmaxyx()
        self.board = Board(size[1], size[0]-1)
        self.snake = Snake((int(size[1]/2), int(size[0]/2)))
        self.apple = Apple(size[1], size[0]-1)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.window.keypad(True)
        self.window.nodelay(True)
        self.window.scrollok(False)

        self.gameover = False

    def update(self):

        # Propagate user inputs
        try:
            userinput = self.window.getkey()
            logging.info(f"userinput: {userinput}")
        except Exception as e:
            userinput = None
        if userinput in INPUT_TO_DIRECTION:
            direction = INPUT_TO_DIRECTION[userinput]
            self.snake.change_dir(direction)

        # Update game object state
        self.snake.update()

        # Did the snake eat the apple?
        snakehead = self.snake.get_head_position()
        if self.apple.overlaps(snakehead):
            self.snake.grow()
            self.apple.move()

        # Check for game over
        if self.board.is_outside_bounds(snakehead) or self.snake.self_intersects():
            self.gameover = True

        if self.gameover:
            logging.info(f"The game is over")
            return

        # Render
        self.window.erase()
        self.board.render(self.window)
        self.snake.render(self.window)
        self.apple.render(self.window)
        self.window.refresh()

    def terminate(self):
        curses.nocbreak()
        self.window.keypad(False)
        curses.echo()
        curses.endwin()
