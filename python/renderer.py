import curses
import exceptions
import logging
from apple import Apple
from board import Board
from directions import Directions, Instructions
from input import Input
from snake import Snake

class Renderer():

    def __init__(self):
        # TODO snake and board should probably be owned by a level or something
        self.window = curses.initscr()
        size = self.window.getmaxyx()
        self.board = Board(size[1], size[0]-1)
        self.snake = Snake((int(size[1]/2), int(size[0]/2)))
        self.apple = Apple(size[1], size[0]-1)
        self.input = Input()
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
            input = self.input.get_input(self.window)
            if isinstance(input, Directions):
                self.snake.change_dir(input)
            elif isinstance(input, Instructions):
                if input == Instructions.SPEED_UP:
                    self.snake.change_speed(0.1)
                elif input == Instructions.SPEED_DOWN:
                    self.snake.change_speed(-0.1)
                elif input == Instructions.TURN_RIGHT or input == Instructions.TURN_LEFT:
                    self.snake.change_dir(input)
        except exceptions.NoInputException:
            pass # Just skip if there's no input

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
            self.board.game_over = True
            self.snake.is_active = False

        # Render
        self.window.erase()
        self.board.render(self.window)
        self.snake.render(self.window)
        self.apple.render(self.window)
        self.input.render(self.window)
        self.window.refresh()

    def terminate(self):
        curses.nocbreak()
        self.window.keypad(False)
        curses.echo()
        curses.endwin()
